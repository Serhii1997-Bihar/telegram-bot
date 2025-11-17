from database.init_sqlite import get_db_connection
import pytz, datetime, telebot

def task_reminder(bot):
    now = datetime.datetime.now(pytz.timezone('Europe/Kiev')).strftime('%d-%m-%Y %H:%M')
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employers")
    users = cur.fetchall()
    for user in users:
        user_id = user[0]
        user_name = user[1]
        table_name = f'tasks_{user_name}'
        cur.execute(f"SELECT * FROM {table_name} WHERE date = ?", (now,))
        task = cur.fetchone()
        if task:
            bot.send_message(user_id, f"Don't forget about {task[2]} 🚨")
            cur.execute(f"DELETE FROM {table_name} WHERE date = ?", (now,))
    conn.commit()
    conn.close()