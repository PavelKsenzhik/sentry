from flask import Flask

app = Flask(__name__)

storage = {}


@app.route("/add/<date>/<int:number>")
def add(date: str, number: int):
    year = int(date[:4])
    month = int(date[4:6])
    day = int(date[6:8])

    storage.setdefault(year, {}).setdefault(month, {}).setdefault(day, 0)
    storage[year].setdefault('total', 0)
    storage[year][month].setdefault('total', 0)

    storage[year][month][day] += number
    storage[year]['total'] += number
    storage[year][month]['total'] += number

    return f'Текущее состояние {storage}'


@app.route("/calculate/<int:year>")
def calculate_year(year: int):
    try:
        res = storage[year]['total']
    except KeyError:
        return  f'Данные за {year} год отсутствуют'
    return f'Затраты за {year} год: {res}'


@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year: int, month: int):
    try:
        res = storage[year][month]['total']
    except KeyError:
        return f'Данные за {year} год {month} месяц отсутствуют'
    return f'Затраты за {year} год {month} месяц: {res}'


# Добавил для облегчения тестирования
@app.route("/get-storage")
def get_storage():
    return f'{storage}'


if __name__ == "__main__":
    app.run(debug=True)
