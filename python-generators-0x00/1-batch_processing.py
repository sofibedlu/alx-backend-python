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

def stream_users_in_batches(batch_size):
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True, buffered=True)
    try:
        cursor.execute("SELECT * FROM user_data")
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
    finally:
        cursor.close()
        connection.close()

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        filtered_users = [user for user in batch if user['age'] > 100]
        # Process the filtered users
        for user in filtered_users:
            print(user)