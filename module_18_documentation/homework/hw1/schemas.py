from marshmallow import validates, post_load
from flasgger import Schema, fields, ValidationError

from models import get_book_by_title, get_author_by_id, Book, Author


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Int(required=True)

    @validates('title')
    def validate_title(self, title: str) -> None:
        if get_book_by_title(title) is not None:
            raise ValidationError(
                'Book with title "{title}" already exists, '
                'please use a different title.'.format(title=title)
            )

    @validates('author')
    def validate_author(self, author: int) -> None:
        if get_author_by_id(author) is None:
            raise ValidationError("Author is not exist")

    @post_load
    def create_book(self, data: dict, **kwargs) -> Book:
        return Book(**data)


class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    middle_name = fields.Str(required=False)

    @post_load
    def create_author(self, data: dict, **kwargs) -> Author:
        return Author(**data)
