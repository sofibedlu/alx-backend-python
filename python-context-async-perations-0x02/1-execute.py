import sqlite3

class ExecuteQuery:
    def __init__(self, query, params=None):
        self.connection = None
        self.cursor = None
        self.query = query
        self.params = params
        self.db_name = 'users.db'

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        if exc_type:
            print(f"An exception occurred: {exc_type}, {exc_value}")
        return False  # Allow exceptions to propagate

        
# Query the database using the reusable context manager
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery(query, params) as cursor:
    rows = cursor.fetchall()
    print("Query Results:")
    for row in rows:
        print(row)
