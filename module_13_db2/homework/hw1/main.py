import sqlite3


sql_request = """
SELECT COUNT(*) FROM 'table_truck_with_vaccine'
    WHERE temperature_in_celsius NOT BETWEEN 16 AND 20 AND truck_number = ?
"""


def check_if_vaccine_has_spoiled(
        cursor: sqlite3.Cursor,
        truck_number: str
) -> bool:
    cursor.execute(sql_request, (truck_number,))
    res_sql = cursor.fetchone()
    return res_sql[0] >= 3


if __name__ == '__main__':
    truck_number: str = input('Введите номер грузовика: ')
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        spoiled: bool = check_if_vaccine_has_spoiled(cursor, truck_number)
        print('Испортилась' if spoiled else 'Не испортилась')
        conn.commit()
