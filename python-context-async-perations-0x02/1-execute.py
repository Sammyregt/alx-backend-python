#!/usr/bin/python3
import sqlite3


class ExecuteQuery:
    def __init__(self, query, param):
        """
        Initialize with a SQL query and optional parameters.

        Args:
            query (str): SQL query string (can include ? placeholders).
            params (tuple | list | any, optional): Values for the placeholders.
                Defaults to None.
        """
        self.query = query
        self.param = param if param is not None else ()

    def __enter__(self):
        """
        Setup method:
        Creates a new SQLite database connection
        when used in a context manager.
        """
        self.conn = sqlite3.connect("users.db")
        cursor = self.conn.cursor()

        if not isinstance(self.params, (tuple, list)):
            self.params = (self.params,)

        cursor.execute(self.query, (self.param,))
        return cursor.fetchall()

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
    query = "SELECT * FROM users WHERE age > ?"
    query_param = 25
    with ExecuteQuery(query=query, param=query_param) as users:
        print(users)