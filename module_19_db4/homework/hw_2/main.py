import sqlite3

query = f"""
SELECT s.full_name, AVG(ag.grade) as avg_grade
from students AS s
JOIN assignments_grades AS ag ON ag.student_id=s.student_id
GROUP BY s.student_id
ORDER BY avg_grade DESC, s.full_name
LIMIT 10
"""


def work():
    with sqlite3.connect('../../homework.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query)

        result = cursor.fetchall()
        print(result)


if __name__ == '__main__':
    work()
