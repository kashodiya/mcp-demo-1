import sqlite3
from datetime import datetime

def init_database():
    conn = sqlite3.connect('bmo_data.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'analyst'
        )
    ''')
    
    # Banks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS banks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aba_code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL
        )
    ''')
    
    # Reports table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bank_id INTEGER NOT NULL,
            report_code TEXT NOT NULL,
            submission_date TEXT NOT NULL,
            has_errors BOOLEAN DEFAULT 0,
            is_accepted BOOLEAN DEFAULT NULL,
            FOREIGN KEY (bank_id) REFERENCES banks (id)
        )
    ''')
    
    # Validation errors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS validation_errors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER NOT NULL,
            error_type TEXT NOT NULL,
            error_message TEXT NOT NULL,
            field_name TEXT,
            FOREIGN KEY (report_id) REFERENCES reports (id)
        )
    ''')
    
    # Error comments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS error_comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            error_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            comment TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (error_id) REFERENCES validation_errors (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully")

def get_db_connection():
    conn = sqlite3.connect('bmo_data.db')
    conn.row_factory = sqlite3.Row
    return conn