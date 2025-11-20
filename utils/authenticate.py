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
    my_id = os.getenv("MY_ID")
    if my_id and user_id == int(my_id):
        return True

    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM employers WHERE user_id = ?", (user_id,))
        return cur.fetchone() is not None

