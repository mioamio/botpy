import sqlite3

def create_db():
    conn = sqlite3.connect('birthdays.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS birthdays (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_birthday(name, date):
    conn = sqlite3.connect('birthdays.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO birthdays (name, date) VALUES (?, ?)', (name, date))
    conn.commit()
    conn.close()

def remove_birthday(name):
    conn = sqlite3.connect('birthdays.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM birthdays WHERE name = ?', (name,))
    conn.commit()
    conn.close()