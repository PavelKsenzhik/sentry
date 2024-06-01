import sqlite3


def task1() -> None:
    with sqlite3.connect("hw_3_database.db") as conn:
        cursor = conn.cursor()

        for i in range(1, 4):
            cursor.execute(f"SELECT COUNT(*) FROM table_{i}")
            result = cursor.fetchall()
            print(f"Записей в таблице table_{i}:", result[0][0])


def task2() -> None:
    with sqlite3.connect("hw_3_database.db") as conn:
        cursor = conn.cursor()

        cursor.execute(f"SELECT COUNT(DISTINCT value) FROM table_1")
        result = cursor.fetchall()
        print("Уникальных записей в таблице table_1:", result[0][0])


def task3() -> None:
    with sqlite3.connect("hw_3_database.db") as conn:
        cursor = conn.cursor()

        cursor.execute(f"SELECT COUNT(table_1.value) FROM table_1 "
                       f"INNER JOIN table_2 on table_2.value=table_1.value")

        result = cursor.fetchall()
        print("Количество записей из table_1, встречающихся в таблице table_2:", result[0][0])


def task4() -> None:
    with sqlite3.connect("hw_3_database.db") as conn:
        cursor = conn.cursor()

        cursor.execute(f"SELECT COUNT(table_1.value) FROM table_1 "
                       f"INNER JOIN table_2 on table_2.value=table_1.value "
                       f"INNER JOIN table_3 on table_3.value=table_1.value")
        result = cursor.fetchall()
        print("Количество записей из table_1, встречающихся в таблицах table_2 и table_3:", result[0][0])


if __name__ == '__main__':
    task1()
    task2()
    task3()
    task4()
