import sqlite3
from datetime import datetime
import functools


def log_queries(func):
    """
    This decorator prints the query argument before
    invoking the original function.
    """
    @functools.wraps(func)
    def wrapper_log_query(query, *args, **kwargs):
        current_time = datetime.now()
        print(f"{current_time} [Query]: {query}")
        return func(query, *args, **kwargs)
    return wrapper_log_query


@log_queries
def fetch_all_users(query):
    """
    This function creates a connection to the database,
    fetches all users and then closes the connection
    to the database
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


if __name__ == "__main__":
    # fetch users while logging the query
    users = fetch_all_users(query="SELECT * FROM users")