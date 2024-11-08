import sqlite3

# Utility functions for handling SQLite operations
class UserDatabase:
    def __init__(self, db_name='users.db'):
        self.db_name = db_name
        self.create_table()

    # Connect to the SQLite database
    def connect_db(self):
        return sqlite3.connect(self.db_name)

    # Create the users table if it doesn't exist
    def create_table(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    # Check if the username already exists
    def username_exists(self, username):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        return user is not None

    # Add a new user to the database
    def add_user(self, username, password):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()

    # Validate the username and password
    def validate_user(self, username, password):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        return user is not None
