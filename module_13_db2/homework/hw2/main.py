import csv
import sqlite3


sql_request = """ 
DELETE FROM 'table_fees'
    WHERE truck_number = ? AND timestamp = ?
"""


def delete_wrong_fees(
        cursor: sqlite3.Cursor,
        wrong_fees_file: str
) -> None:
    with open(wrong_fees_file) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            cursor.execute(sql_request, (row[0], row[1]))


if __name__ == "__main__":
    with sqlite3.connect("../homework.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        delete_wrong_fees(cursor, "../wrong_fees.csv")
        conn.commit()
