from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from database.init_db import init_db  # <-- import this

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'devkey')
DB_PATH = 'database/inventory.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ... [login_required, admin_required, routes remain unchanged]

if __name__ == '__main__' or os.environ.get("RENDER") == "true":
    if not os.path.exists('database'):
        os.makedirs('database')

    # Always run init_db on startup
    init_db()

    app.run(debug=True)
