import random
import sqlite3


football_commands = [
    ("Ювентус", "Турин"),
    ("Барселона", "Барселона"),
    ("РеалМадрид", "Мадрид"),
    ("МанчестерЮнайтед", "Манчестер"),
    ("Челси", "Лондон"),
    ("Арсенал", "Лондон"),
    ("ЦСКА", "Москва"),
    ("Ливерпуль", "Ливерпуль"),
    ("Зенит", "Санкт-Петербург"),
    ("Спартак", "Москва"),
    ("Милан", "Милан"),
    ("Бавария", "Мюнхен"),
    ("БоруссияД", "Дортмунд"),
    ("Локомотив", "Москва"),
    ("Интер", "Милан"),
    ("Анжи", "Махачкала"),
    ("Рома", "Рим"),
    ("Валенсия", "Валенсия"),
    ("МанчестерСити", "Англия"),
]

football_rating = [1, 2, 2,  3]

sql_request_for_table_uefa_commands = """
INSERT INTO 'uefa_commands' 
(command_number, command_name, command_country, command_level) VALUES (?, ?, ?, ?)
"""

sql_request_for_table_uefa_draw = """
INSERT INTO 'uefa_draw' (command_number, group_number) VALUES (?, ?)
"""

sql_request_drop = """
DELETE FROM 'uefa_commands';
DELETE FROM 'uefa_draw';
"""


def generate_test_data(
        cursor: sqlite3.Cursor,
        number_of_groups: int
) -> None:
    cursor.executescript(sql_request_drop)

    commands = []
    draws = []
    command_id = 1

    for i in range(number_of_groups):
        for i_rating in football_rating:
            command = random.choice(football_commands)
            commands.append((command_id, command[0], command[1], i_rating))
            draws.append((command_id, i + 1))
            command_id += 1

    cursor.executemany(sql_request_for_table_uefa_commands, commands)
    cursor.executemany(sql_request_for_table_uefa_draw, draws)


if __name__ == '__main__':
    number_of_groups: int = int(input('Введите количество групп (от 4 до 16): '))
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        generate_test_data(cursor, number_of_groups)
        conn.commit()
