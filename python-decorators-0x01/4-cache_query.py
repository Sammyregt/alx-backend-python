import time
import sqlite3
import functools

with_db_connection = __import__("1-with_db_connection").with_db_connection

query_cache = {}


def cache_query(func):
    """
    This decorator returns the cached value of a
    query if it exists in the query cache
    """
    @functools.wraps(func)
    def wrapper_cache(query, *args, **kwargs):
        if query in query_cache:
            print(f"Fetched from Cache: {query}")
            return query_cache[query]
        else:
            result = func(query=query, *args, **kwargs)
            query_cache[query] = result
            print(f"Fetched from DB: {query}")
            return result
    return wrapper_cache
            

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


if __name__ == "__main__":
    # First call will cache the result
    users = fetch_users_with_cache(query="SELECT * FROM users")

    # Second call will use the cached result
    users_again = fetch_users_with_cache(query="SELECT * FROM users")