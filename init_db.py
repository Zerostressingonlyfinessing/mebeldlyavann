import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price TEXT,
    material TEXT,
    image_main TEXT,
    image_1 TEXT,
    image_2 TEXT,
    image_3 TEXT
)
''')

conn.commit()
conn.close()

print("Таблица 'items' успешно создана.")
