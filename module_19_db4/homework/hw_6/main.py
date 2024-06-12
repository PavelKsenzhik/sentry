import sqlite3

query = f"""
SELECT AVG(ag.grade) AS avg_grade
FROM assignments AS a
JOIN assignments_grades AS ag on ag.assisgnment_id=a.assisgnment_id
WHERE a.assignment_text LIKE 'прочитать%' OR a.assignment_text LIKE 'выучить%'
"""


def work():
    with sqlite3.connect('../../homework.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query)

        result = cursor.fetchall()
        print(result)


if __name__ == '__main__':
    work()
