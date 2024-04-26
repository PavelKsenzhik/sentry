"""
Ваш коллега, применив JsonAdapter из предыдущей задачи, сохранил логи работы его сайта за сутки
в файле skillbox_json_messages.log. Помогите ему собрать следующие данные:

1. Сколько было сообщений каждого уровня за сутки.
2. В какой час было больше всего логов.
3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
4. Сколько сообщений содержит слово dog.
5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
"""
import itertools
from typing import Dict
import json
import subprocess


with open('skillbox_json_messages.log') as log_file:
    logs = [json.loads(line) for line in log_file.readlines()]


def task1() -> Dict[str, int]:
    """
     1. Сколько было сообщений каждого уровня за сутки.
     @return: словарь вида {уровень: количество}
     """

    result = dict()

    for log in logs:
        level = log["level"]
        if result.get(level):
            result[level] += 1
        else:
            result[level] = 1
    return result


def task2() -> int:
    """
    2. В какой час было больше всего логов.
    @return: час
    """
    logs_by_hour = {}
    for hour, log_group in itertools.groupby(logs, key=lambda x: x["time"].split(":")[0]):
        logs_by_hour[hour] = len(list(log_group))
    return max(logs_by_hour, key=logs_by_hour.get)


def task3() -> int:
    """
    3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
    @return: количество логов
    """
    command = ["grep", "-c", 'time": "05:[0-1][0-9]:[0-5][0-9]", "level": "CRITICAL"', "skillbox_json_messages.log"]
    result = subprocess.run(command, capture_output=True, text=True)
    output = int(result.stdout.strip())
    return output


def task4() -> int:
    """
    4. Сколько сообщений содержат слово dog.
    @return: количество сообщений
    """
    command = ["grep", "-c", 'message": ".* dog .*"', "skillbox_json_messages.log"]
    result = subprocess.run(command, capture_output=True, text=True)
    output = int(result.stdout.strip())
    return output


def task5() -> str:
    """
    5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
    @return: слово
    """
    result = {}
    for i_message in [i_log["message"].split(' ') for i_log in logs if i_log["level"] == 'WARNING']:
        for i_word in i_message:
            if i_word in result:
                result[i_word] = result[i_word] + 1
            else:
                result[i_word] = 1

    return max(result, key=result.get)


if __name__ == '__main__':
    tasks = (task1, task2, task3, task4, task5)
    for i, task_fun in enumerate(tasks, 1):
        task_answer = task_fun()
        print(f'{i}. {task_answer}')
