from database.init_sqlite import get_db_connection

def is_registered(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employers WHERE user_id = ?", (user_id,))
    return cur.fetchone() is not None