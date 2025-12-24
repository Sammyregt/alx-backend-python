#!/usr/bin/python3

connect_to_prodev = __import__('seed').connect_to_prodev

def stream_users_in_batches(batch_size):
    """
    Create a generator that streams rows 
    from an SQL database in batches.

    """
    connection = connect_to_prodev()

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        rows = cursor.fetchmany(batch_size)
        if rows == []:
            break
        yield rows

def batch_processing(batch_size):
    """
    Function that processes each batch to filter
    users over the age of 25
    
    :param batch_size: Number of rows per batch
    """
    filtered_users = []
    for batch in stream_users_in_batches(batch_size):
        for row in batch:
            if row.get("age") > 25:
                filtered_users.append(row)
                print(row)
    return filtered_users