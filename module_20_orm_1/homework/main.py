from flask import jsonify, Flask, request

from module_20_orm_1.homework.models import Books, ReceivingBooks

app = Flask(__name__)


@app.route('/books', methods=['GET'])
def get_all_books():
    return Books.get_all()


@app.route('/debtors', methods=['GET'])
def get_debtors():
    return ReceivingBooks.get_debtors(14)


@app.route('/issue_book', methods=['POST'])
def issue_book():
    book_id = request.json.get('book_id')
    student_id = request.json.get('student_id')

    try:
        ReceivingBooks.issue_book(book_id, student_id)
        return jsonify({"message": "Book issued successfully"})
    except Exception as ex:
        return jsonify({"error": str(ex)})


@app.route('/return_book', methods=['POST'])
def return_book():
    book_id = request.json.get('book_id')
    student_id = request.json.get('student_id')

    try:
        ReceivingBooks.return_book(book_id, student_id)
        return jsonify({"message": "Book returned successfully"})
    except Exception as ex:
        return jsonify({"error": str(ex)})


if __name__ == '__main__':
    app.run(debug=True)
