import sqlite3

query = f"""
SELECT a.group_id, AVG(ag.grade) avg_grade, MIN(ag.grade) min_grade, MAX(ag.grade) max_grade 
FROM assignments as a
JOIN assignments_grades as ag on ag.assisgnment_id=a.assisgnment_id
WHERE ag.date > a.due_date
GROUP BY a.group_id
"""


def work():
    with sqlite3.connect('../../homework.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query)

        result = cursor.fetchall()
        print(result)


if __name__ == '__main__':
    work()
