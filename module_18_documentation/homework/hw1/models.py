import sqlite3
from dataclasses import dataclass
from typing import Optional, Union, List, Dict

DATA = {
    'authors': [
        {'id': 1, 'first_name': 'Swaroop', 'last_name': 'C.', 'middle_name': 'H.'},
        {'id': 2, 'first_name': 'Herman', 'last_name': 'Melville', 'middle_name': ''},
        {'id': 3, 'first_name': 'Leo', 'last_name': 'Tolstoy', 'middle_name': ''}
    ],
    'books': [
        {'id': 1, 'title': 'A Byte of Python', 'author': 1},
        {'id': 2, 'title': 'Moby-Dick; or, The Whale', 'author': 2},
        {'id': 3, 'title': 'War and Peace', 'author': 3},
    ]
}

DATABASE_NAME = 'table_books.db'
BOOKS_TABLE_NAME = 'books'
AUTHORS_TABLE_NAME = 'authors'


@dataclass
class Author:
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


@dataclass
class Book:
    title: str
    author: Optional[Union[int, Author]]
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


def init_db(initial_records: List[Dict]) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT name FROM sqlite_master 
                WHERE type='table' AND name='{BOOKS_TABLE_NAME}';
            """
        )
        exists = cursor.fetchone()
        if not exists:
            cursor.executescript(
                f"""
                CREATE TABLE IF NOT EXISTS '{AUTHORS_TABLE_NAME}' (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    middle_name VARCHAR(50)
                );
                """
            )
            cursor.executescript(
                f"""
                CREATE TABLE `{BOOKS_TABLE_NAME}`(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT,
                    author INTEGER REFERENCES '{AUTHORS_TABLE_NAME}'(id) ON DELETE CASCADE 
                );
                """
            )
            cursor.executemany(
                f"""
                INSERT INTO `{AUTHORS_TABLE_NAME}` 
                (first_name, last_name, middle_name) VALUES (?, ?, ?)
                """,
                [
                    (item['first_name'], item['last_name'], item['middle_name'])
                    for item in initial_records['authors']
                ]
            )
            cursor.executemany(
                f"""
                INSERT INTO `{BOOKS_TABLE_NAME}`
                (title, author) VALUES (?, ?)
                """,
                [
                    (item['title'], item['author'])
                    for item in initial_records['books']
                ]
            )


def _get_author_obj_from_row(row: tuple) -> Author:
    return Author(id=row[0], first_name=row[1], last_name=row[2], middle_name=row[3])


def _get_book_obj_from_row(row: tuple) -> Book:
    return Book(id=row[0], title=row[1], author=row[2])


def get_book_by_title(book_title: str) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE title = ?
            """,
            (book_title,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def get_author_by_id(author_id: int) -> Optional[Author]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{AUTHORS_TABLE_NAME}` WHERE id = ?
            """,
            (author_id,)
        )
        author = cursor.fetchone()
        if author:
            return _get_author_obj_from_row(author)


def get_author_by_fio(first_name: str, last_name: str, middle_name: Optional[str]) -> Optional[Author]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{AUTHORS_TABLE_NAME}` 
            WHERE first_name = ? AND last_name = ? middle_name = ?
            """,
            (first_name, last_name, middle_name)
        )
        author = cursor.fetchone()
        if author:
            return _get_author_obj_from_row(author)


def get_all_books() -> list[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM `{BOOKS_TABLE_NAME}`')
        all_books = cursor.fetchall()
        return [_get_book_obj_from_row(row) for row in all_books]


def add_book(book: Book) -> Book:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO `{BOOKS_TABLE_NAME}` 
            (title, author) VALUES (?, ?)
            """,
            (book.title, book.author)
        )
        book.id = cursor.lastrowid
        return book


def update_book(book: Book) -> Book:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE `{BOOKS_TABLE_NAME}` 
            SET title = ?, author = ?
            WHERE id = ?;
            """,
            (book.title, book.author, book.id)
        )
        return book


def get_book_by_id(book_id: int) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE id = ?
            """,
            (book_id,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def delete_book_by_id(book_id: int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM {BOOKS_TABLE_NAME}
            WHERE id = ?
            """,
            (book_id,)
        )
        conn.commit()


def get_all_authors() -> list[Author]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM `{AUTHORS_TABLE_NAME}`')
        all_items = cursor.fetchall()
        return [_get_author_obj_from_row(row) for row in all_items]


def add_author(author: Author) -> Author:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO `{AUTHORS_TABLE_NAME}` 
            (first_name, last_name, middle_name) 
            VALUES (?, ?, ?)
            """,
            (author.first_name, author.last_name, author.middle_name)
        )
        author.id = cursor.lastrowid
        return author


def update_author(author: Author) -> Author:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE `{Author}`
            SET first_name = ?, last_name = ?, middle_name = ?
            WHERE id = ?;
            """,
            (author.first_name, author.last_name, author.middle_name, author.id)
        )
        return author


def delete_author_by_id(author_id: int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM `{AUTHORS_TABLE_NAME}` WHERE id = ?
            """,
            (author_id,)
        )


def get_books_by_author(author_id: int) -> list[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` 
            WHERE author = ?
            """,
            (author_id,)
        )
        all_books = cursor.fetchall()
        return [_get_book_obj_from_row(row) for row in all_books]
