import datetime
import random
import os

from flask import Flask

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')

cars_list = ['Chevrolet', 'Renault', 'Ford', 'Lada']
cats_list = ['корниш-рекс', 'русская голубая', 'шотландская вислоухая', 'мейн-кун', 'манчкин']
@app.route('/hello_world')
def hello_world():
    return "Привет, мир!"


@app.route('/cars')
def cars():
    return ', '.join(cars_list)


@app.route('/cats')
def cats():
    return random.choice(cats_list)


@app.route('/get_time/now')
def time_now():
    time = datetime.datetime.now()
    current_time = time.strftime("%H.%M.%S")

    return "Точное время: {current_time}".format(
        current_time=current_time
    )


@app.route('/get_time/future')
def get_time_future():
    time_delta = datetime.timedelta(hours=1)
    datetime_after_hour = datetime.datetime.now() + time_delta
    time_after_hour = datetime_after_hour.strftime("%H.%M.%S")

    return "Точное время через час будет {current_time_after_hour}".format(
        current_time_after_hour=time_after_hour
    )


@app.route('/get_random_word')
def get_random_word():
    text = ''
    book = open(BOOK_FILE)
    text = book.read()

    return text

#
# @app.route('/counter')
# def test_function():
#     pass
#
#
if __name__ == '__main__':
    app.run(debug=True)
