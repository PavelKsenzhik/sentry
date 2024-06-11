import operator
from flask import Flask
from flask_jsonrpc import JSONRPC

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)


@jsonrpc.method('calc.add')
def add(a: float, b: float) -> float:
    """
    Пример запроса:

    $ curl -i -X POST -H "Content-Type: application/json; indent=4" \
        -d '{
            "jsonrpc": "2.0",
            "method": "calc.add",
            "params": {"a": 7.8, "b": 5.3},
            "id": "1"
        }' http://localhost:5000/api

    Пример ответа:

    HTTP/1.1 200 OK
    Server: Werkzeug/2.2.2 Python/3.10.6
    Date: Fri, 09 Dec 2022 19:00:09 GMT
    Content-Type: application/json
    Content-Length: 54
    Connection: close

    {
      "id": "1",
      "jsonrpc": "2.0",
      "result": 13.1
    }
    """
    return operator.add(a, b)


@jsonrpc.method('calc.sub')
def add(a: float, b: float) -> float:
    """
        Пример запроса:

        $ curl -i -X POST -H "Content-Type: application/json; indent=4" \
            -d '{
                "jsonrpc": "2.0",
                "method": "calc.sub",
                "params": {"a": 7.8, "b": 5.3},
                "id": "1"
            }' http://localhost:5000/api

        Пример ответа:

        HTTP/1.1 200 OK
        Server: Werkzeug/2.2.2 Python/3.10.6
        Date: Fri, 09 Dec 2022 19:00:09 GMT
        Content-Type: application/json
        Content-Length: 54
        Connection: close

        {
          "id": "1",
          "jsonrpc": "2.0",
          "result": 2.5
        }
    """
    return operator.sub(a, b)


@jsonrpc.method('calc.mul')
def add(a: float, b: float) -> float:
    """
        Пример запроса:

        $ curl -i -X POST -H "Content-Type: application/json; indent=4" \
            -d '{
                "jsonrpc": "2.0",
                "method": "calc.mul",
                "params": {"a": 2.0, "b": 3.0},
                "id": "1"
            }' http://localhost:5000/api

        Пример ответа:

        HTTP/1.1 200 OK
        Server: Werkzeug/2.2.2 Python/3.10.6
        Date: Fri, 09 Dec 2022 19:00:09 GMT
        Content-Type: application/json
        Content-Length: 54
        Connection: close

        {
          "id": "1",
          "jsonrpc": "2.0",
          "result": 6.0
        }
    """
    return operator.mul(a, b)


@jsonrpc.method('calc.div')
def add(a: float, b: float) -> float:
    """
        Пример запроса:

        $ curl -i -X POST -H "Content-Type: application/json; indent=4" \
            -d '{
                "jsonrpc": "2.0",
                "method": "calc.div",
                "params": {"a": 6.0, "b": 3.0},
                "id": "1"
            }' http://localhost:5000/api

        Пример ответа:

        HTTP/1.1 200 OK
        Server: Werkzeug/2.2.2 Python/3.10.6
        Date: Fri, 09 Dec 2022 19:00:09 GMT
        Content-Type: application/json
        Content-Length: 54
        Connection: close

        {
          "id": "1",
          "jsonrpc": "2.0",
          "result": 2.0
        }
    """
    return operator.truediv(a, b)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)