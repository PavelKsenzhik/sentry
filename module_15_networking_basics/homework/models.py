import datetime
import sqlite3
from typing import Optional, Any


class Room:
    def __init__(self,
                 id: Optional[int],
                 floor: int,
                 beds: int,
                 guest_num: int,
                 price: int):
        self.id: int = id
        self.floor: int = floor
        self.beds: int = beds
        self.guest_num: int = guest_num
        self.price: int = price

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


class Order:
    def __init__(self,
                 id: Optional[int],
                 check_in: datetime,
                 check_out: datetime,
                 first_name: str,
                 last_name: str,
                 room_id: int):
        self.id = id
        self.check_in: datetime = check_in
        self.check_out: datetime = check_out
        self.first_name = first_name
        self.last_name = last_name
        self.room_id = room_id


def init_db() -> None:
    with sqlite3.connect('hotel.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS `rooms` (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    floor INTEGER, 
                    beds INTEGER,
                    guest_num INTEGER,
                    price INTEGER
                );
            """
        )

        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS `orders` (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    check_in DATETIME,
                    check_out DATETIME,
                    first_name VARCHAR(255),
                    last_name VARCHAR(255),
                    room_id INTEGER,
                    FOREIGN KEY (room_id) REFERENCES rooms(id))
            """
        )


def add_new_room(room: Room) -> int:
    with sqlite3.connect('hotel.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        query = """
            INSERT INTO rooms (floor, beds, guest_num, price)
            VALUES (?, ?, ?, ?)
        """

        cursor.execute(query, (room.floor, room.beds, room.guest_num, room.price))
        conn.commit()

        cursor.execute("SELECT MAX(id) FROM rooms")
        return cursor.fetchone()[0]


def get_all_rooms() -> list[Room]:
    with sqlite3.connect('hotel.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        cursor.execute(
            """
                SELECT * FROM `rooms`
            """
        )

        return [Room(*row) for row in cursor.fetchall()]


def get_rooms(check_in: datetime, check_out: datetime, guest_num: int) -> list[Room]:
    with sqlite3.connect('hotel.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        query = """
                SELECT rooms.id, floor, beds, guest_num, price FROM rooms
                LEFT JOIN `orders` on orders.room_id=rooms.id
                WHERE rooms.id not in (SELECT room_id FROM orders) 
                or (orders.check_out < ? or orders.check_in > ?) AND rooms.guest_num >= ?;
         """

        cursor.execute(query, (check_in, check_out, guest_num))

        return [Room(*row) for row in cursor.fetchall()]


def get_room_not_free(check_in: datetime, check_out: datetime, room_id: int) -> bool:
    with sqlite3.connect('hotel.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        query = """
                SELECT COUNT(*) FROM `orders` 
                WHERE check_in >= ? AND check_out <= ? AND room_id = ?;
         """

        cursor.execute(query, (check_in, check_out, room_id))

        return cursor.fetchone()[0] > 0


def add_order(order: Order):
    with sqlite3.connect('hotel.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        query = """
            INSERT INTO `orders` (check_in, check_out, first_name, last_name, room_id) 
            VALUES  (?, ?, ?, ?, ?)
        """

        cursor.execute(query, (order.check_in, order.check_out, order.first_name, order.last_name, order.room_id))
        conn.commit()

        cursor.execute("SELECT MAX(id) FROM orders")
        return cursor.fetchone()[0]
