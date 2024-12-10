import sqlite3 

class DatabaseConnection():
    def __init__(self, db_name):
        self.connection = None
        self.db_name = db_name

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        return self.connection
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()
        if exc_type:
            print(f"Exception has been handled: {exc_type}, {exc_value}, {traceback}")
            return True # Suppress the exception
        
db_name = 'users.db'

# Querying the database
with DatabaseConnection(db_name) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    for user in users:
        print(user)