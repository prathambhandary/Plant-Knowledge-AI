import sqlite3

conn = sqlite3.connect('users.db')  # creates or opens plants.db
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS user_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')
conn.commit()

cursor.execute("SELECT * FROM user_details")
rows = cursor.fetchall()
for row in rows:
    5
    # print(row)

def verify_user(email, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM user_details WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    
    conn.close()
    
    return user is not None

def add_user(name, email, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO user_details (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Email already exists
    finally:
        conn.close()

def email_exists(email):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM user_details WHERE email = ?", (email,))
    exists = cursor.fetchone() is not None

    conn.close()
    return exists

import sqlite3

def get_name_by_email(email):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM user_details WHERE email = ?", (email,))
    result = cursor.fetchone()
    
    conn.close()

    if result:
        return result[0]  # returns the name
    else:
        return None  # no user found with that email
