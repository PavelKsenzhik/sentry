import datetime
import random
import os
import re

from flask import Flask

app = Flask(__name__)

CARS_LIST = ['Chevrolet', 'Renault', 'Ford', 'Lada']
CATS_LIST = ['корниш-рекс', 'русская голубая', 'шотландская вислоухая', 'мейн-кун', 'манчкин']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')

counter_integer = 0
war_and_peace_book = ''


@app.route('/hello_world')
def hello_world():
    return "Привет, мир!"


@app.route('/cars')
def cars():
    return ', '.join(CARS_LIST)


@app.route('/cats')
def cats():
    return random.choice(CATS_LIST)


@app.route('/get_time/now')
def time_now():
    time = datetime.datetime.now()
    current_time = time.strftime("%H.%M.%S")

    return f"Точное время: {current_time}"


@app.route('/get_time/future')
def get_time_future():
    datetime_after_hour = datetime.datetime.now() + datetime.timedelta(hours=1)
    time_after_hour = datetime_after_hour.strftime("%H.%M.%S")

    return f"Точное время через час будет {time_after_hour}"


def get_book_words(book):
    return re.findall('\w+', book)


@app.route('/get_random_word')
def get_random_word():
    global war_and_peace_book

    if war_and_peace_book == '':
        with open(BOOK_FILE, 'r', encoding='utf-8') as book:
            war_and_peace_book = book.read()

    words = get_book_words(war_and_peace_book)

    return random.choice(words)


@app.route('/counter')
def counter():
    global counter_integer

    counter_integer += 1
    return str(counter_integer)


if __name__ == '__main__':
    app.run(debug=True)
