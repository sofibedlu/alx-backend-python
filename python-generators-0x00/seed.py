import mysql.connector
import csv
import uuid

host = "localhost"
user = "alxpd_user"
password = "password"
db_name = "ALX_prodev"

def connect_db():
    # Connect to the MySQL server
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )

def create_database(connection):
    # Create the ALX_prodev database if it does not exist
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()

def connect_to_prodev():
    # Connect to the ALX_prodev database
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )

def create_table(connection):
    # Create the user_data table if it does not exist
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(4,1) NOT NULL,
            INDEX (user_id)
        )
    """)
    cursor.close()

def insert_data(connection, data):
    cursor = connection.cursor()
    with open(data, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            cursor.execute("""
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE name=VALUES(name), email=VALUES(email), age=VALUES(age)
            """, (str(uuid.uuid4()), row['name'], row['email'], row['age']))
    connection.commit()
    cursor.close()
