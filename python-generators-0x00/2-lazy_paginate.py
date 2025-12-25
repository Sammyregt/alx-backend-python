#!/usr/bin/python3

connect_to_prodev = __import__('seed').connect_to_prodev


def paginate_users(page_size, offset):
    """
    This function fetches a paginated list of users from the database.
    """

    connection = connect_to_prodev()

    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset};"
    )
    rows = cursor.fetchall()
    connection.close()
    return rows

def lazy_paginate(page_size):
    """
    Generator that yields users in a paginated manner.

    :param page_size: Number of users per page
    """
    current_page = 0
    while True:
        users = paginate_users(page_size, offset=(page_size * current_page))
        if not users:
            break
        for user in users:
            yield user
        current_page += 1