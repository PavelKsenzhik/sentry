import sqlite3

query = f"""
SELECT sg.group_id, 
    COUNT(s.student_id) AS students_count, 
    AVG(ag.grade) AS avg_grade, 
    SUM(CASE WHEN ag.grade IS NULL THEN 1 ELSE 0 END) AS unchecked_count,
    SUM(CASE WHEN a.due_date < ag.date THEN 1 ELSE 0 END) AS late_checked_count
FROM students_groups AS sg
LEFT JOIN students AS s ON s.group_id=sg.group_id
LEFT JOIN assignments AS a ON a.group_id=sg.group_id
LEFT JOIN assignments_grades AS ag ON ag.assisgnment_id=a.assisgnment_id AND ag.student_id=s.student_id
GROUP BY sg.group_id
"""


def work():
    with sqlite3.connect('../../homework.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query)

        result = cursor.fetchall()
        print(result)


if __name__ == '__main__':
    work()
