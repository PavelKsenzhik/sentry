import os

from flask import Flask, render_template, request, Response
from typing import List

from models import init_db, get_all_books, DATA, Book, add_book, AddBookForm, ShowAuthorForm, get_books_by_author, \
    get_book_by_id, update_count_book, update_count_many_books

app: Flask = Flask(__name__)


def _get_html_table_for_books(books: List[dict]) -> str:
    table = """
<table>
    <thead>
    <tr>
        <th>ID</td>
        <th>Title</td>
        <th>Author</td>
    </tr>
    </thead>
    <tbody>
        {books_rows}
    </tbody>
</table>
"""
    rows: str = ''
    for book in books:
        rows += '<tr><td>{id}</tb><td>{title}</tb><td>{author}</tb></tr>'.format(
            id=book['id'], title=book['title'], author=book['author'],
        )
    return table.format(books_rows=rows)


@app.route('/books')
def all_books() -> str:
    books = get_all_books()
    update_count_many_books(books)
    return render_template(
        'index.html',
        books=books,
    )


@app.route('/books/author', methods=['GET', 'POST'])
def get_books_for_author() -> Response:
    if request.method == 'GET':
        return render_template('get_author.html')
    elif request.method == "POST":
        form = ShowAuthorForm()
        if not form.validate_on_submit():
            return Response(form.errors, status=400)

        books = get_books_by_author(form.author.data)
        update_count_many_books(books)
        return render_template(
            'index.html',
            books=books,
        )

    return Response(status=415)


@app.route('/books/<id>', methods=['GET'])
def get_book(id: int) -> Response:
    book = get_book_by_id(id)
    if book:
        update_count_book(book)

    return render_template("details.html", book=book)


@app.route('/books/form', methods=['GET', 'POST'])
def books_form() -> Response:
    if request.method == 'GET':
        return render_template('add_book.html')
    elif request.method == "POST":
        form = AddBookForm()
        if not form.validate_on_submit():
            return Response(form.errors, status=400)

        add_book(Book(title=form.book_title.data, author=form.author_name.data, id=None))
        return all_books()

    return Response(status=415)


if __name__ == '__main__':
    init_db(DATA)

    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
