import sqlite3
import csv

db_name = 'users.db'

with sqlite3.connect(db_name) as conn:
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')
    conn.commit()


csv_file = 'user_data.csv'

with sqlite3.connect(db_name) as conn:
    cursor = conn.cursor()
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute('''
                INSERT INTO users (name, email, age)
                VALUES (?, ?, ?)
            ''', (row['name'], row['email'], row['age']))
    conn.commit()