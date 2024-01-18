"""
Реализуйте endpoint /hello-world/<имя>, который возвращает строку «Привет, <имя>. Хорошей пятницы!».
Вместо хорошей пятницы endpoint должен уметь желать хорошего дня недели в целом, на русском языке.

Пример запроса, сделанного в субботу:

/hello-world/Саша  →  Привет, Саша. Хорошей субботы!
"""

from flask import Flask
from datetime import datetime

app = Flask(__name__)

WEEKDAYS_TUPLE = ('понедельника', 'вторника', 'среды', 'четверга', 'пятницы', 'субботы', 'воскресенья')

@app.route('/hello-world/<username>')
def hello_world(username):
    weekday = datetime.today().weekday()
    if weekday == 2 or weekday == 4 or weekday == 5:
        wish_end = 'й'
    else:
        wish_end = 'го'

    return f"Привет, {username}. Хороше{wish_end} {WEEKDAYS_TUPLE[weekday]}!"


if __name__ == '__main__':
    app.run(debug=True)