import sqlite3


def task1() -> None:
    with sqlite3.connect("hw_4_database.db") as conn:
        cursor = conn.cursor()

        cursor.execute(f"SELECT COUNT(*) FROM salaries "
                       f"WHERE salary < 5000")
        result = cursor.fetchall()
        print(f"Число жителей, находящихся за чертой бедности:", result[0][0])


def task2() -> None:
    with sqlite3.connect("hw_4_database.db") as conn:
        cursor = conn.cursor()

        cursor.execute(f"SELECT AVG(salary) FROM salaries")
        result = cursor.fetchall()
        print(f"Средняя зп:", result[0][0])


def task3() -> None:
    with sqlite3.connect("hw_4_database.db") as conn:
        cursor = conn.cursor()

        cursor.execute(f"SELECT salary FROM salaries ORDER BY salary "
                       f"LIMIT 1 OFFSET (SELECT COUNT(*) FROM salaries) / 2")
        result = cursor.fetchall()
        print(f"Медианная зп:", result[0][0])


def task4() -> None:
    with sqlite3.connect("hw_4_database.db") as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(salary) FROM salaries")
        total = cursor.fetchone()[0]
        cursor.execute(f"SELECT SUM(salary) FROM (SELECT * FROM salaries ORDER BY salary DESC LIMIT 0.1 * {total})")
        top10 = cursor.fetchone()[0]
        cursor.execute(f"SELECT SUM(salary) FROM (SELECT * FROM salaries ORDER BY salary ASC LIMIT 0.9 * {total})")
        other = cursor.fetchone()[0]
        print("Число социального неравенства F:", round(top10 / other * 100, 2))

        cursor.execute(f"SELECT ROUND(10000 * "
                       f"(SELECT SUM(salary) FROM (SELECT * FROM salaries ORDER BY salary DESC LIMIT 0.1 * (SELECT COUNT(salary) FROM salaries)))"
                       f" / "
                       f"(SELECT SUM(salary) FROM (SELECT * FROM salaries ORDER BY salary ASC LIMIT 0.9 * (SELECT COUNT(salary) FROM salaries)))"
                       f", 2) / 100")
        result = cursor.fetchall()
        print(f"Число социального неравенства F:", result[0][0])


if __name__ == '__main__':
    task1()
    task2()
    task3()
    task4()
