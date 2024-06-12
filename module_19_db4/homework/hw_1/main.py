import sqlite3

query = f"""
SELECT t.full_name, AVG(ag.grade) as avg_grade
from teachers AS t
JOIN assignments AS a ON a.teacher_id=t.teacher_id
JOIN assignments_grades AS ag ON ag.assisgnment_id=a.assisgnment_id
GROUP BY t.teacher_id
ORDER BY avg_grade
LIMIT 1;
"""


def work():
    with sqlite3.connect('../../homework.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query)

        result = cursor.fetchall()
        print(result)


if __name__ == '__main__':
    work()
