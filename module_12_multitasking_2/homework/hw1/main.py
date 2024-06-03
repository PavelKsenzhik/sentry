import threading
import requests
import sqlite3
import time
import multiprocessing
from multiprocessing.pool import ThreadPool


def get_person(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None

    data = response.json()
    person = {
        'name': data['name'],
        'age': data['birth_year'],
        'gender': data['gender']
    }
    return person


def save_person(person):
    if not person:
        return

    with sqlite3.connect("people.db") as conn:
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO people (name, age, gender) "
                       f"VALUES ('{person['name']}', '{person['age']}', '{person['gender']}')")
        conn.commit()


def work(url):
    person = get_person(url)
    save_person(person)


def work_with_pool():
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        pool.map(work, [f'https://swapi.dev/api/people/{i}/' for i in range(1, 21)])


def work_thread_pool():
    with ThreadPool(processes=multiprocessing.cpu_count()) as pool:
        pool.map(work, [f'https://swapi.dev/api/people/{i}/' for i in range(1, 21)])


def execute_func(name, func):
    start_time = time.time()
    func()
    end_time = time.time()
    print(f"Name: {name}.Execution time: {end_time - start_time} seconds")


def create_database():
    with sqlite3.connect("people.db") as conn:
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS people '
                       '(Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT, age TEXT, gender TEXT);')
        conn.commit()


def main():
    create_database()

    execute_func('with_pool', work_with_pool)
    execute_func('with_thread_pool', work_thread_pool)


if __name__ == '__main__':
    main()
