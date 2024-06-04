import sqlite3


sql_request_salary_worker = """
SELECT salary FROM 'table_effective_manager' WHERE name = ?
"""

sql_request_update_salary = """
UPDATE 'table_effective_manager' SET salary = ? WHERE name = ?
"""

sql_request_delete_worker = """
DELETE FROM 'table_effective_manager' WHERE name = ?
"""


def get_ivan_sovin_salary(cursor: sqlite3.Cursor) -> int:
    cursor.execute(sql_request_salary_worker, ("Иван Совин",))
    return cursor.fetchone()[0]

def ivan_sovin_the_most_effective(
        cursor: sqlite3.Cursor,
        name: str,
) -> None:
    cursor.execute(sql_request_salary_worker, (name, ))
    salary = cursor.fetchone()[0]

    print("Зарплата сотрудника составляет:", salary)

    new_slary = salary * 1.1
    if new_slary > salary_ivan_sovin:
        cursor.execute(sql_request_delete_worker, (name, ))
        print(f"Зарплата оказалась высокой и сотрудник {name} был уволен")
    else:
        cursor.execute(sql_request_update_salary, (new_slary, name))
        print(f"Зарплата сотрудника {name} была повышена и сейчас составляет {new_slary}")


if __name__ == '__main__':
    name: str = input('Введите имя сотрудника: ')
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        salary_ivan_sovin = get_ivan_sovin_salary(cursor)

        ivan_sovin_the_most_effective(cursor, name)
        conn.commit()
