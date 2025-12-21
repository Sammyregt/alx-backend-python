#!/usr/bin/python3

"""
Docstring for python-generators-0x00.seed
seed.py

This script:
1. Connects to a MySQL server using credentials from a .env file.
2. Create the ALX_prodev database if  it does not exist.
3. Connects to the ALX_prodev database.
4. Creates the user_data table
5. Inserts user records from a csv file into the user_data table
"""

# import necessary modules

# importing MySQL connector to interact with the MySQL database
import mysql.connector

# importing the load_dotenv function to load environment variables from the .env file
from dotenv import load_dotenv

#importing csv to read data from csv file
import csv

import os

# loading environment variables from the .env file
load_dotenv()

def connect_db():
    try:
        connection = mysql.connector.connect(
            host = os.getenv("DB_HOST"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD")
        )
        return connection
    except Exception as e:
        print(f"Error connecting to MySQL server: {e}")
        return None


def create_database(connection):
    """
    creates the ALX_prodev database if it does not exist

    Args:
        connection: Active MySQL connection 
    """
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()

def connect_to_prodev():
    """
    Connects to the ALX_prodev database

    Uses the DB_NAME from the .env file to connect to the database
    Returns:
        connection: Active MySQL connection to ALX_prodev database
    """
    connection = mysql.connector.connect(
        host = os.getenv("DB_HOST"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        database = os.getenv("DB_NAME")
    )
    return connection

def create_table(connection):
    """
    Creates the user_data table in the ALX_prodev database

    Args:
        connection: Active MySQL connection to ALX_prodev database
    """
    cursor = connection.cursor()

    # SQL statement to create table
    user_record = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
        name VARCHAR(50) NOT NULL,
        email VARCHAR(50) NOT NULL,
        age DECIMAL(3,0) NOT NULL
    )
    """

    # Execute table creation query
    cursor.execute(user_record)

    # Close cursor
    cursor.close()

def insert_data(connection, data):
    """
    Inserts records from a csv file into the user_data table

    Args:
        connection: Active MySQL connection to ALX_prodev database
        data: Path to the CSV file
    """
    cursor = connection.cursor()

    # Open the CSV file in read mode
    with open(data, mode='r', newline='') as file:
        csv_reader = csv.reader(file)

        # Skip the header row
        header = next(csv_reader, None)

        # convert remaining rows into tuples
        records = [tuple(row) for row in csv_reader]

        # SQL statement to insert data into user_data table
        cursor.executemany(
            "INSERT INTO user_data (name, email, age) VALUES (%s, %s, %s)", records
        )

    # Commit changes to the database
    connection.commit()

    # Close cursor
    cursor.close()
