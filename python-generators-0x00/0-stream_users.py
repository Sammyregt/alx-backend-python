#!/usr/bin/python3

connect_to_prodev = __import__('seed').connect_to_prodev

def stream_users():
    """
    Create a generator that streams rows 
    from an SQL database one by one.

    """
    connection = connect_to_prodev()

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data")

    while True:
        row = cursor.fetchone()
        if row is None:
            break
        yield row