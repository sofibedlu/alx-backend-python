#!/usr/bin/python3
seed = __import__('seed')

def stream_user_ages():
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        yield row['age']
    connection.close()


def calculate_avg_age():
    total, count = 0, 0
    for age in stream_user_ages():
        total += age
        count += 1
    print('Average age of users: {}'.format(total / count))


if __name__ == '__main__':
    calculate_avg_age()