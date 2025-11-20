from database.init_sqlite import get_db_connection

def get_users(bot, call):
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT user_id, username, city, phone FROM employers")
        rows = cur.fetchall()
        for user in rows:
            bot.send_message(call.message.chat.id, f"<code>{user[0]}</code> | {user[1]} | {user[2]} | {user[3]}", parse_mode='HTML')

def choose_user(bot, call):
    msg = bot.send_message(call.message.chat.id, 'Put user_id:')
    bot.register_next_step_handler(msg, remove_user, bot)

def remove_user(message, bot):
    user_id = message.text
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM employers WHERE user_id = ?", (user_id,))
        conn.commit()

    bot.send_message(message.chat.id, 'User has been deleted')


