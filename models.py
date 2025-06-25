
import sqlite3
import os

DB_NAME = 'database.db'

def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('CREATE TABLE messages (id INTEGER PRIMARY KEY, content TEXT)')
        c.execute('INSERT INTO messages (content) VALUES (?)', ("Добро пожаловать!",))
        conn.commit()
        conn.close()

def get_message():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT content FROM messages WHERE id=1')
    message = c.fetchone()[0]
    conn.close()
    return message
