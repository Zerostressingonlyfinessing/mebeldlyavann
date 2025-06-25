#!/usr/bin/env python3
import sqlite3

DB_NAME = 'database.db'

def init_db():
    """Создает таблицу items, если её ещё нет."""
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price TEXT,
            description TEXT,
            material TEXT,
            image_main TEXT,
            image_1 TEXT,
            image_2 TEXT,
            image_3 TEXT
        )
        """)
    print(f"Таблица `items` в базе `{DB_NAME}` инициализирована или уже существует.")

if __name__ == '__main__':
    init_db()
