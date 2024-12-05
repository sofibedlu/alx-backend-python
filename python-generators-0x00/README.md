# Python Generators Project

This project demonstrates various techniques for processing and streaming user data from a MySQL database using Python generators. The project includes scripts for streaming users, batch processing, and lazy pagination.


## Files

### `0-stream_users.py`

This script streams all users from the `user_data` table in the database.

- **Functions:**
  - `connect_to_prodev()`: Connects to the `ALX_prodev` database.
  - `stream_users()`: Yields each user row from the `user_data` table.

### `1-batch_processing.py`

This script processes users in batches.

- **Functions:**
  - `connect_to_prodev()`: Connects to the `ALX_prodev` database.
  - `stream_users_in_batches(batch_size)`: Yields batches of users.
  - `batch_processing(batch_size)`: Processes users in batches and filters users older than 25.

### `2-lazy_paginate.py`

This script demonstrates lazy pagination of users.

- **Functions:**
  - `paginate_users(page_size, offset)`: Fetches a page of users.
  - `lazy_pagination(page_size)`: Yields pages of users.

### `4-stream_ages.py`

This script streams user ages and calculates the average age.

- **Functions:**
  - `stream_user_ages()`: Yields ages of users.
  - `calculate_avg_age()`: Calculates and prints the average age of users.

### `seed.py`

This script sets up the database and inserts data from a CSV file.

- **Functions:**
  - `connect_db()`: Connects to the MySQL server.
  - `create_database(connection)`: Creates the `ALX_prodev` database if it does not exist.
  - `connect_to_prodev()`: Connects to the `ALX_prodev` database.
  - `create_table(connection)`: Creates the `user_data` table if it does not exist.
  - `insert_data(connection, data)`: Inserts data from a CSV file into the `user_data` table.

### `test/`

This directory contains test scripts for the main scripts.

- **`0-main.py`**: Tests the `seed.py` script.
- **`1-main.py`**: Tests the `0-stream_users.py` script.
- **`2-main.py`**: Tests the `1-batch_processing.py` script.
- **`3-main.py`**: Tests the `2-lazy_paginate.py` script.

### `user_data.csv`

This file contains sample user data to be inserted into the database.

## Setup and Usage

1. **Install Dependencies:**
   Ensure you have MySQL and the `mysql-connector-python` package installed.

   ```sh
   pip install mysql-connector-python