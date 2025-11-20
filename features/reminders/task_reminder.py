from database.init_sqlite import get_db_connection
import pytz, datetime, sqlite3

def task_reminder(bot):
    now = datetime.datetime.now(pytz.timezone('Europe/Kiev')).strftime('%d-%m-%Y %H:%M')

    with get_db_connection() as conn:
        cur = conn.cursor()

        cur.execute("SELECT user_id FROM employers")
        users = cur.fetchall()

        for user in users:
            user_id = user[0]
            cur.execute("SELECT task_id, task FROM tasks WHERE user_id = ? AND date = ?", (user_id, now))
            task = cur.fetchone()

            if task:
                bot.send_message(user_id, f"Don't forget about {task[1]} 🚨")
                cur.execute("DELETE FROM tasks WHERE task_id = ?", (task[0],))

        conn.commit()


