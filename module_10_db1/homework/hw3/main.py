import sqlite3

DB_PATH = 'hw_3_database.db'


def count_entries(table_name):
    with sqlite3.connect(DB_PATH) as connect:
        cursor = connect.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        result = cursor.fetchall()
    return result[0][0]


def count_desctinct_entries(table_name):
    with sqlite3.connect(DB_PATH) as connect:
        cursor = connect.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name} DISTINCT")
        result = cursor.fetchall()
    return result[0][0]


if __name__ == '__main__':
    tables = ['table_1', 'table_2', 'table_3']

    for table_name in tables:
        print(f"Количество записей в {table_name}", count_entries(table_name))

    print(f"Количество уникальных записей в {table_name}", count_entries(table_name))
    count_desctinct_entries(tables[0])
