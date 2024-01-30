"""
Напишите GET-эндпоинт /uptime, который в ответ на запрос будет выводить строку вида f"Current uptime is {UPTIME}",
где UPTIME — uptime системы (показатель того, как долго текущая система не перезагружалась).

Сделать это можно с помощью команды uptime.
"""

from flask import Flask

app = Flask(__name__)


def get_uptime_seconds() -> float:
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])

    return uptime_seconds


def get_uptime_str() -> str:
    uptime_total_seconds = get_uptime_seconds()
    uptime_minutes = int(uptime_total_seconds / 60)
    uptime_seconds = int(uptime_total_seconds - uptime_minutes * 60)

    return f'{uptime_minutes} minutes and {uptime_seconds} seconds'


@app.route("/uptime", methods=['GET'])
def uptime() -> str:
    return f"Current uptime is {get_uptime_str()}"


if __name__ == '__main__':
    app.run(debug=True)
