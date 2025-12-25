#!/usr/bin/python3
import sqlite3
import csv


def connect_db():
    """
    Create a connection to SQLite database
    """
    connection = sqlite3.connect('users.db')
    return connection


def create_table(connection):
    """
    Create a table with tablename 'user_data'
    if it does not exist
    """
    cursor = connection.cursor()

    user_record = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(50) NOT NULL,
        email VARCHAR(50) NOT NULL,
        age DECIMAL(3,0) NOT NULL
    )
    """

    cursor.execute(user_record)


def insert_data(connection, data):
    """
    Insert data into the 'user_data' table if
    it does not exist
    """
    cursor = connection.cursor()

    with open(data, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader, None)
        records = [tuple(row) for row in csv_reader]
        cursor.executemany(
            'INSERT INTO users (name, email, age) VALUES (?, ?, ?)',
            records
        )
    connection.commit()

if __name__ == '__main__':
    connection = connect_db()
    create_table(connection=connection)
    insert_data(connection=connection, data='user_data.csv')
    connection.close()