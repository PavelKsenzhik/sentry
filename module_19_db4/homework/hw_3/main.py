import sqlite3

query = f"""
SELECT s.full_name
FROM students AS s
JOIN students_groups AS sg ON sg.group_id=s.group_id
WHERE sg.teacher_id IN (
    SELECT a.teacher_id
    FROM assignments AS a
    JOIN assignments_grades AS ag ON ag.assisgnment_id=a.assisgnment_id
    GROUP BY a.group_id
    ORDER BY AVG(ag.grade)
    LIMIT 1
);
"""


def work():
    with sqlite3.connect('../../homework.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query)

        result = cursor.fetchall()
        print(result)


if __name__ == '__main__':
    work()
