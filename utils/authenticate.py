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
    if int(os.getenv('MY_ID')) == user_id:
        return True
    else:
        return False
