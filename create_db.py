import sqlite3
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS USER(
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )
''')
conn.commit()
conn.close()