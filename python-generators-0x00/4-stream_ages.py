#!/usr/bin/python3

connect_to_prodev = __import__('seed')

def stream_user_ages():
    """
    Create a generatot to compute a memory-efficient
    aggregate function i.e average age of a large dataset
    """
    connection = connect_to_prodev.connect_to_prodev()

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")

    while True:
        user = cursor.fetchone()
        if user is None:
            break
        yield user["age"]


def compute_average_age():
    """
    Function that computes the average age
    of users in the database.
    """
    total_age = 0
    user_count = 0

    for age in stream_user_ages():
        total_age += age
        user_count += 1

    average_age = total_age / user_count if user_count > 0 else 0
    return average_age

if __name__ == "__main__":
    average_age = compute_average_age()
    print(f"Average age of users: {average_age}")