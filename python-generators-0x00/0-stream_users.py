import mysql.connector

host = "localhost"
user = "alxpd_user"
password = "password"
db_name = "ALX_prodev"

def connect_to_prodev():
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )

def stream_users():
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row
    cursor.close()
    connection.close()
