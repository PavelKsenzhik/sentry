import logging

from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flasgger import APISpec, Swagger
from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import ValidationError
from werkzeug.serving import WSGIRequestHandler

from models import (
    DATA,
    get_all_books,
    init_db,
    add_book,
    get_book_by_id,
    delete_book_by_id,
    add_author,
    get_books_by_author,
    delete_author_by_id, update_book, get_all_authors, update_author,
)
from schemas import BookSchema, AuthorSchema

# logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
api = Api(app)

spec = APISpec(
    title="BoockList",
    version="1.0.0",
    openapi_version="2.0",
    plugins=[
        FlaskPlugin(),
        MarshmallowPlugin(),
    ]
)


class BookList(Resource):
    def get(self) -> tuple[list[dict], int]:
        """
           Return all books
           ---
           tags:
             - books
           responses:
             200:
               description: books list
               schema:
                 type: array
                 items:
                   $ref: '#/definitions/Book'

        """

        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200

    def post(self) -> tuple[dict, int]:
        """
            Add new book.
            ---
            tags:
              - books
            parameters:
              - in: body
                name: new book
                schema:
                  $ref: '#/definitions/Book'
            responses:
              201:
                descriptions: New book created
                schema:
                  $ref: '#/definitions/Book'
        """

        data = request.json
        schema = BookSchema()
        try:
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        book = add_book(book)
        return schema.dump(book), 201


class BookItem(Resource):
    def put(self, id: int):
        """
            Update book by id.
            ---
            tags:
              - books
            parameters:
              - in: path
                name: book id
              - in: body
                name: book
                schema:
                  $ref: '#/definitions/Book'
            responses:
              200:
                descriptions: updated book
                schema:
                  $ref: '#/definitions/Book'
        """

        data = request.json
        schema = BookSchema()
        try:
            book = schema.load(data)
            book.id = id
            update_book(book)
            return schema.dump(book), 200
        except ValidationError as e:
            return e.messages, 400

    def get(self, id: int):
        """
            Get book by id.
            ---
            tags:
              - books
            parameters:
              - in: path
                name: book id
            responses:
              200:
                descriptions: book
                schema:
                  $ref: '#/definitions/Book'
        """

        schema = BookSchema()
        book = get_book_by_id(id)
        return schema.dump(book), 200

    def delete(self, id: int):
        """
            Delete book by id.
            ---
            tags:
              - books
            parameters:
              - in: path
                name: book id
        """

        delete_book_by_id(id)
        return {'msg': "ok"}, 200


class AuthorList(Resource):
    def get(self) -> tuple[list[dict], int]:

        schema = AuthorSchema()
        return schema.dump(get_all_authors(), many=True), 200

    def post(self):
        data = request.json
        schema = AuthorSchema()
        try:
            author = schema.load(data)
            add_author(author)
            return schema.dump(author), 200
        except ValidationError as exc:
            return exc.messages, 400


class AuthorItem(Resource):
    def put(self, id: int):
        data = request.json
        schema = AuthorSchema()
        try:
            author = schema.load(data)
            author.id = id
            update_author(author)
            return schema.dump(author), 200
        except ValidationError as e:
            return e.messages, 400

    def get(self, id: int) -> tuple[list[dict], int]:
        schema = BookSchema()
        return schema.dump(get_books_by_author(id), many=True), 200

    def delete(self, id: int):
        delete_author_by_id(id)
        return {"msg": "ok"}, 200


api.add_resource(BookList, '/api/books')
api.add_resource(BookItem, '/api/books/<int:id>')
api.add_resource(AuthorList, '/api/authors')
api.add_resource(AuthorItem, '/api/authors/<int:id>')

# template = spec.to_flasgger(
#     app,
#     definitions=[BookSchema, AuthorSchema],
# )
#
# swagger = Swagger(app, template=template)
swagger = Swagger(app, template_file='./swagger.json')

if __name__ == '__main__':
    init_db(initial_records=DATA)

    # WSGIRequestHandler.protocol_version = "HTTP/1.0"
    app.run(debug=True)
