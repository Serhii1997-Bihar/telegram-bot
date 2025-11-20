from database.init_sqlite import get_db_connection

def get_users():
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM employers")
        rows = cur.fetchall()

        return rows