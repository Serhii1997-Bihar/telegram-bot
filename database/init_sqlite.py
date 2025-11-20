import sqlite3, os

current_directory = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_directory, 'db_bot.db')

def init_db():
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS employers (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                city TEXT NOT NULL,
                year INTEGER NOT NULL,
                phone TEXT NOT NULL
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                task TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES employers(user_id)
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                author TEXT NOT NULL,
                book TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES employers(user_id)
            )
        ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS read_books (
                read_book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                author TEXT NOT NULL,
                book TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES employers(user_id)
            )
        ''')
        conn.commit()

def get_db_connection():
    conn = sqlite3.connect(db_path, check_same_thread=False)
    return conn