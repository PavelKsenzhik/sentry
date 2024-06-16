import time


class WSGIApp:
    def __init__(self):
        self.routes = {}

    def route(self, path):
        def decorator(func):
            def wrapped_handler(environ, start_response):
                status = '200 OK'
                response_headers = [('Content-type', 'text/plain')]
                start_response(status, response_headers)
                variables = self.retrieve_variables(environ.get('PATH_INFO'), path)
                return [func(**variables).encode()]

            self.routes[path] = wrapped_handler
            return wrapped_handler

        return decorator

    def not_found(self, environ, start_response):
        status = '404 Not Found'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        return [b'Not Found']

    def retrieve_variables(self, path, route):
        parts = path.strip('/').split('/')
        route_parts = route.strip('/').split('/')
        if len(parts) != len(route_parts):
            return None

        return {route_part.strip('<>').split('/')[0]: part
                for route_part, part in zip(route_parts, parts)
                if route_part.startswith('<') and route_part.endswith('>')}

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO')
        handler = self.routes.get(path)
        if handler is None:
            for route, func in self.routes.items():
                variables = self.retrieve_variables(path, route)
                if variables:
                    handler = func
                    break

        handler = handler or self.not_found
        return handler(environ, start_response)


application = WSGIApp()


@application.route('/hello')
def hello():
    return 'Hello World!'


@application.route('/hello/<name>')
def hello_name(name):
    return f'Hello {name}!'


@application.route('/long_task')
def long_task():
    time.sleep(300)
    return 'We did it!'
