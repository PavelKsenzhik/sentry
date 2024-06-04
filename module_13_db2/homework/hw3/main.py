import datetime
import sqlite3


generate_hw3_sql = """
CREATE TABLE IF NOT EXISTS `birds`(
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    date VARCHAR(255) NOT NULL
);
"""

sql_request_check_availability_in_table = """
SELECT EXISTS(SELECT * FROM `birds` WHERE name = ? AND date != ?)
"""

sql_request_add_bird = """ 
INSERT INTO `birds` (name, date) VALUES (?, ?);
"""


def log_bird(
        cursor: sqlite3.Cursor,
        bird_name: str,
        date_time: str,
) -> None:
    cursor.execute(sql_request_add_bird, (bird_name, date_time))
    print(f"Птица {bird_name} записана в журнал")


def check_if_such_bird_already_seen(
        cursor: sqlite3.Cursor,
        bird_name: str,
        date_time: str,
) -> bool:
    cursor.execute(sql_request_check_availability_in_table, (bird_name, date_time))
    res = cursor.fetchone()
    return res[0]


def create_table(cursor: sqlite3.Cursor) -> None:
    cursor.executescript(generate_hw3_sql)


if __name__ == "__main__":
    print("Программа помощи ЮНатам v0.1")
    name: str = input("Пожалуйста введите имя птицы\n> ")
    count_str: str = input("Сколько птиц вы увидели?\n> ")
    count: int = int(count_str)
    right_now: str = datetime.datetime.utcnow().isoformat()

    with sqlite3.connect("../homework.db") as connection:
        cursor: sqlite3.Cursor = connection.cursor()

        create_table(cursor)
        connection.commit()

        log_bird(cursor, name, right_now)

        if check_if_such_bird_already_seen(cursor, name, right_now):
            print("Такую птицу мы уже наблюдали!")
