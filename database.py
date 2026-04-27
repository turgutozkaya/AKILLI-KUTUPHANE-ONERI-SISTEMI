import sqlite3

def connect():
    return sqlite3.connect("library.db")

def setup_database():
    """Tabloları oluşturur (Eğer yoksa)"""
    conn = connect()
    cursor = conn.cursor()
    
    # ID'ler AUTOINCREMENT, isimler UNIQUE yapılarak hatalar önlendi
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        category TEXT,
        author TEXT
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        book_id INTEGER,
        rating INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(book_id) REFERENCES books(id)
    )""")
    
    conn.commit()
    conn.close()