import time
import sqlite3 
import functools

with_db_connection = __import__('1-with_db_connection').with_db_connection

#### paste your with_db_decorator here
def retry_on_failure(retries=3, delay=2):
    """
    A decorator that retries a function upon failure.
    
    :retries: Number of retry attempts
    :delay: Delay in seconds between retries
    """
    def retry_decorator(func):
        @functools.wraps(func)
        def wrapper_retry(*args, **kwargs):
            last_exceptio = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f'Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...')
                    time.sleep(delay)
            raise last_exception
        return wrapper_retry
    return retry_decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure
if __name__ == "__main__":
    users = fetch_users_with_retry()
    print(users)