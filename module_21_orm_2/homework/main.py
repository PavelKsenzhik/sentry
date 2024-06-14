import datetime

from flask import jsonify, Flask, request

from module_21_orm_2.homework.models import Books, ReceivingBooks, Students

app = Flask(__name__)


@app.route('/books', methods=['GET'])
def get_all_books():
    """ Return all books """

    return Books.get_all()


@app.route('/books/total/<int:author_id>', methods=['GET'])
def get_count_books_by_author(author_id):
    """ Return count books for author """

    try:
        return Books.get_count_books_by_author(author_id)
    except Exception as ex:
        return jsonify({"error": str(ex)})


@app.route('/books/unread_by_student/<int:student_id>', methods=['GET'])
def get_unread_books_by_student(student_id):
    """ Return books witch student don't read """

    try:
        return Books.get_unread_books_by_student(student_id)
    except Exception as ex:
        return jsonify({"error": str(ex)})


@app.route('/books/average_books_per_month', methods=['GET'])
def get_average_books_per_month():
    """ Return average number of books students borrowed this month """

    now = datetime.datetime.now()
    return ReceivingBooks.get_average_books_per_month(now.year, now.month)


@app.route('/books/most_popular', methods=['GET'])
def get_most_popular_book():
    """ Return the most popular book among students with a GPA greater than 4.0 """

    return Books.get_most_popular_book(4.0)


@app.route('/students/top_readers', methods=['GET'])
def get_top_readers():
    """ TOP 10 most reading students this year """

    return Students.get_top_readers()


@app.route('/debtors', methods=['GET'])
def get_debtors():
    """ Return debtors books """

    return ReceivingBooks.get_debtors(14)


@app.route('/issue_book', methods=['POST'])
def issue_book():
    """ Take book """

    book_id = request.json.get('book_id')
    student_id = request.json.get('student_id')

    try:
        ReceivingBooks.issue_book(book_id, student_id)
        return jsonify({"message": "Book issued successfully"})
    except Exception as ex:
        return jsonify({"error": str(ex)})


@app.route('/return_book', methods=['POST'])
def return_book():
    """ Return book """

    book_id = request.json.get('book_id')
    student_id = request.json.get('student_id')

    try:
        ReceivingBooks.return_book(book_id, student_id)
        return jsonify({"message": "Book returned successfully"})
    except Exception as ex:
        return jsonify({"error": str(ex)})


@app.route('/students/bulk_insert', methods=['POST'])
def bulk_insert_students():
    if 'file' not in request.files:
        return jsonify({"error": "File not found"})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "File not select"})
    if not file.filename.endswith('.csv'):
        return jsonify({"error": "File have incorrect format"})

    try:
        students_data = file.read().decode('utf-8').split('\n')
        students_data = [row.split(';') for row in students_data if row]
        students_dicts = []

        for row in students_data:
            student_dict = {
                'name': row[0].strip(),
                'surname': row[1].strip(),
                'phone': row[2].strip(),
                'email': row[3].strip(),
                'average_score': float(row[4].strip()),
                'scholarship': True if row[5].strip().lower() == 'true' else False
            }
            students_dicts.append(student_dict)

        Students.bulk_insert(students_dicts)
        return jsonify({"message": "Students added successfully"})
    except Exception as ex:
        return jsonify({"error": str(ex)})


if __name__ == '__main__':
    app.run(debug=False)
