from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'devkey')
DB_PATH = 'database/inventory.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def login_required(view):
    def wrapped_view(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    wrapped_view.__name__ = view.__name__
    return wrapped_view

def admin_required(view):
    def wrapped_view(*args, **kwargs):
        if session.get('role') != 'admin':
            flash('Admin access required.')
            return redirect(url_for('index'))
        return view(*args, **kwargs)
    wrapped_view.__name__ = view.__name__
    return wrapped_view

@app.route('/')
@login_required
def index():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM inventory').fetchall()
    conn.close()
    return render_template('index.html', items=items, role=session.get('role'))

@app.route('/add', methods=['POST'])
@login_required
@admin_required
def add():
    name = request.form['name']
    quantity = request.form['quantity']
    conn = get_db_connection()
    conn.execute('INSERT INTO inventory (name, quantity) VALUES (?, ?)', (name, quantity))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:item_id>')
@login_required
@admin_required
def delete(item_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM inventory WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['role'] = user['role']
            return redirect('/')
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    if not os.path.exists('database'):
        os.makedirs('database')
    app.run(debug=True)
