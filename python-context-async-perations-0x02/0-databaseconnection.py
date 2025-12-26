#!/usr/bin/python3
import sqlite3


class DatabaseConnection:
    def __init__(self):
        pass
    
    def __enter__(self):
        """
        Setup method:
        Creates a new SQLite database connection
        when used in a context manager.
        """
        self.conn = sqlite3.connect("users.db")
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Teardown method:
        - Commits if no exception occurred
        - Rolls back if an error occurred
        - Always closes the connection
        """
        if hasattr(self, "conn"):
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()


if __name__ == "__main__":
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        print(users)