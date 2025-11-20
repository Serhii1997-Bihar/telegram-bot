from database.init_sqlite import get_db_connection

def get_users():
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT username FROM employers")
        rows = cur.fetchall()
        return [row[0] for row in rows]