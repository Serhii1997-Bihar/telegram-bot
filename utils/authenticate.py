from database.init_sqlite import get_db_connection
from dotenv import load_dotenv
import os

load_dotenv()

def is_registered(user_id):
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM employers WHERE user_id = ?", (user_id,))
        return cur.fetchone() is not None


def is_admin(user_id):
    if user_id == os.getenv('MY_ID'):
        return True

    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM employers WHERE user_id = ?", (user_id,))
        return cur.fetchone() is not None
