import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('database/inventory.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        quantity INTEGER NOT NULL
    )
''')
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('admin', 'staff'))
    )
''')
admin_password = generate_password_hash('admin123')
c.execute('INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)',
          ('admin', admin_password, 'admin'))
conn.commit()
conn.close()
