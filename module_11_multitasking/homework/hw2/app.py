import threading
import requests
import sqlite3
import time


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


def work(base_url, people_id):
    url = f'{base_url}/{people_id}/'
    person = get_person(url)
    save_person(person)


def work_without_thread():
    for i in range(1, 21):
        work('https://swapi.dev/api/people', i)


def work_with_thread():
    threads = []
    for i in range(1, 21):
        thread = threading.Thread(target=work, args=('https://swapi.dev/api/people', i))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


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

    execute_func('without_thread', work_without_thread)
    execute_func('with_thread', work_with_thread)


if __name__ == '__main__':
    main()
