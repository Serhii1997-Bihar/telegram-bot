from database.init_sqlite import get_db_connection

def create_task(bot, call, user_id):
    bot_message = bot.send_message(call.message.chat.id, 'Enter the date in the format DD-MM-YYYY HH:MM, and I will remind you about it.')
    bot.register_next_step_handler(bot_message, lambda msg: get_deadline(bot, msg, user_id))

def get_deadline(bot, message, user_id):
    deadline = message.text
    bot_message = bot.send_message(message.chat.id, '📋 Describe your task')
    bot.register_next_step_handler(bot_message, lambda msg: add_to_db(bot, msg, deadline, user_id))

def add_to_db(bot, message, deadline, user_id):
    task = message.text
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tasks (user_id, date, task) VALUES (?, ?, ?)",
            (user_id, deadline, task)
        )
        conn.commit()
    bot.send_message(message.chat.id, '➕ Task created!')


def show_tasks(bot, call, user_id):
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT task_id, task, date FROM tasks WHERE user_id = ?", (user_id,))
        tasks = cur.fetchall()

    if tasks:
        elements = ""
        for element in tasks:
            elements += f"🏷️{element[0]} | {element[1]} | {element[2]}\n"
        bot.send_message(call.message.chat.id, elements)
    else:
        bot.send_message(call.message.chat.id, "❌ You don't have any tasks.")

def choose_task(bot, call, user_id):
    bot_message = bot.send_message(call.message.chat.id, 'Enter task number 🔍')
    bot.register_next_step_handler(bot_message, lambda msg: remove_task(bot, msg, user_id))

def remove_task(bot, message, user_id):
    task_id = message.text
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM tasks WHERE task_id = ? AND user_id = ?", (task_id, user_id))
        conn.commit()
    bot.send_message(message.chat.id, 'Task has been removed!')

