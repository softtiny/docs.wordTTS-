import sqlite3

connection = sqlite3.connect('.tmp/example.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER
)
''')

connection.commit()
cursor.close()
connection.close()