from datetime import datetime, timedelta

import sqlalchemy
from flask import jsonify
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, backref
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, Boolean, func, extract, ForeignKey, desc

engine = create_engine('sqlite:///library.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


# таблица книг в библиотеке
class Books(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    author = relationship('Authors', back_populates="books")
    received_books = relationship("ReceivingBooks", lazy='selectin', back_populates="book",
                                  cascade='all, delete-orphan')

    def __repr__(self):
        return f"{self.name}, {self.count}, {self.release_date}, {self.author_id}"

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def get_all(cls):
        result = session.query(Books).all()
        result_list = [i_item.to_json() for i_item in result]
        return jsonify(result_list)

    @classmethod
    def get_count_books_by_author(cls, author_id):
        book_count = session.query(func.sum(Books.count)).filter(Books.author_id == author_id).scalar()
        return jsonify({"result": book_count})

    @classmethod
    def get_unread_books_by_student(cls, student_id):
        student = session.query(Students).filter(Students.id == student_id).first()
        if student is None:
            raise Exception("Student not found")

        author_ids = [i_book.author_id for i_book in student.books]
        book_ids = [i_book.id for i_book in student.books]

        result = session.query(Books).filter(Books.author_id.in_(author_ids), Books.id.notin_(book_ids)).all()

        result_list = [i_item.to_json() for i_item in result]
        return jsonify(result_list)

    @classmethod
    def get_most_popular_book(cls, score):
        students = session.query(Students).filter(Students.average_score > score).all()
        student_ids = [i_student.id for i_student in students]

        result = session.query(ReceivingBooks)\
            .group_by(ReceivingBooks.book_id)\
            .filter(ReceivingBooks.student_id.in_(student_ids))\
            .order_by(desc(ReceivingBooks.book_id))\
            .first()

        if result is None:
            raise Exception("Book not found")

        return result.book.to_json()


# таблица авторов
class Authors(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    books = relationship('Books', lazy='joined', back_populates='author', cascade='all, delete-orphan')

    def __repr__(self):
        return f"{self.name}, {self.surname}"

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# таблица читателей
class Students(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)
    received_books = relationship("ReceivingBooks", lazy='selectin', back_populates="student",
                                  cascade='all, delete-orphan')
    books = association_proxy('received_books', 'book')

    def __repr__(self):
        return f"{self.name}, {self.surname}, {self.phone}, {self.email}, {self.average_score}, {self.scholarship}"

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def get_students_with_scholarship(cls):
        result = session.query(Students).filter(Students.scholarship).all()
        result_list = [i_item.to_json() for i_item in result]
        return jsonify(result_list)

    @classmethod
    def get_students_with_higher_average_score(cls, score):
        result = session.query(Students).filter(Students.average_score > score).all()
        result_list = [i_item.to_json() for i_item in result]
        return jsonify(result_list)

    @classmethod
    def get_top_readers(cls):
        current_year = datetime.now().year

        result = session.query(ReceivingBooks)\
            .group_by(ReceivingBooks.student_id)\
            .filter(extract('year', ReceivingBooks.date_of_issue) == current_year)\
            .order_by(desc(func.count()))\
            .limit(10).all()
        result_list = [i_item.student.to_json() for i_item in result]
        return jsonify(result_list)

    @classmethod
    def bulk_insert(cls, students_dicts):
        try:
            session.bulk_insert_mappings(Students, students_dicts)
            session.commit()
        except Exception as e:
            session.rollback()
            raise Exception("Added error")


# таблица выдачи книг студентам
class ReceivingBooks(Base):
    __tablename__ = 'receiving_books'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    date_of_issue = Column(Date, nullable=False)
    date_of_return = Column(Date)
    book = relationship("Books", back_populates="received_books", single_parent=True)
    student = relationship("Students", back_populates="received_books", single_parent=True)

    def __repr__(self):
        return f"{self.book_id}, {self.student_id}, {self.date_of_issue}, {self.date_of_return}"

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @hybrid_property
    def count_date_with_book(self):
        date_of_return = self.date_of_return if self.date_of_return else datetime.now()
        days = func.trunc((extract('epoch', date_of_return) - extract('epoch', self.date_of_issue)) / 3600 / 24)
        return days

    @classmethod
    def get_debtors(cls, days):
        result = session.query(ReceivingBooks).filter(ReceivingBooks.count_date_with_book > days).all()
        result_list = [i_item.to_json() for i_item in result]
        return jsonify(result_list)

    @classmethod
    def issue_book(cls, book_id, student_id):
        book = session.query(Books).filter(Books.id == book_id).first()
        if book is None:
            raise Exception("Book not found")
        if book.count <= 0:
            raise Exception("Have not free book")

        student = session.query(Students).filter(Students.id == student_id).first()
        if student is None:
            raise Exception("Student not found")

        book.count -= 1

        new_item = ReceivingBooks(book_id=book_id, student_id=student_id, date_of_issue=datetime.now())
        session.add(new_item)

        session.commit()

    @classmethod
    def return_book(cls, book_id, student_id):
        book = session.query(Books).filter(Books.id == book_id).first()
        if book is None:
            raise Exception("Book not found")

        student = session.query(Students).filter(Students.id == student_id).first()
        if student is None:
            raise Exception("Student not found")

        receiving_book = session.query(ReceivingBooks)\
            .filter(ReceivingBooks.student_id == student_id,
                    ReceivingBooks.book_id == book_id,
                    ReceivingBooks.date_of_return == None)\
            .first()
        if receiving_book is None:
            raise Exception("Receiving book not found")

        book.count += 1
        receiving_book.date_of_return = datetime.now()

        session.commit()

    @classmethod
    def get_average_books_per_month(cls, year, month):
        student_count = session.query(func.count(Students.id)).scalar()

        books_count = session.query(func.count(ReceivingBooks.id)).filter(
            extract('month', ReceivingBooks.date_of_issue) == month,
            extract('year', ReceivingBooks.date_of_issue) == year,
        ).scalar()

        average = books_count / student_count if student_count else 0
        return jsonify({"average_books_per_month": average})


def initialize_db():
    Base.metadata.create_all(bind=engine)

    # Add authors
    author1 = Authors(name='John', surname='Doe')
    author2 = Authors(name='Jane', surname='Smith')

    # Add books
    book1 = Books(name='Book 1', release_date=datetime(2020, 1, 15), author=author1)
    book2 = Books(name='Book 2', release_date=datetime(2019, 5, 20), author=author2)
    book3 = Books(name='Book 3', release_date=datetime(2019, 5, 20), author=author2)

    # Add students
    student1 = Students(name='Alice', surname='Johnson', phone='123456789', email='alice@example.com',
                        average_score=85.0, scholarship=True)
    student2 = Students(name='Bob', surname='Smith', phone='987654321', email='bob@example.com',
                        average_score=78.0, scholarship=False)

    session.add_all([author1, author2])
    session.add_all([book1, book2, book3])
    session.add_all([student1, student2])

    session.commit()
    session.close()


if __name__ == '__main__':
    initialize_db()
