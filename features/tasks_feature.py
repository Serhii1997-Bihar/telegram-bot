from database.init_sqlite import get_db_connection

def create_task(bot, call, user_name):
    table_name = f'tasks_{user_name}'
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (number INTEGER PRIMARY KEY AUTOINCREMENT, "
                f"date TEXT NOT NULL, task TEXT NOT NULL)")
    conn.commit()

    bot_message = bot.send_message(call.message.chat.id, 'Enter the date in the format DD-MM-YYYY HH:MM, and I will remind you about it.')
    bot.register_next_step_handler(bot_message, lambda msg: get_deadline(bot, msg, table_name))

def get_deadline(bot, message, table_name):
    deadline = message.text
    bot_message = bot.send_message(message.chat.id, '📋 Describe your task')
    bot.register_next_step_handler(bot_message, lambda msg: add_to_db(bot, msg, deadline, table_name))

def add_to_db(bot, message, deadline, table_name):
    task = message.text
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"INSERT INTO {table_name} (date, task) VALUES (?, ?)", (deadline, task))
    conn.commit()
    bot.send_message(message.chat.id, '➕ Task created!')

def show_tasks(bot, call, user_name):
    table_name = f'tasks_{user_name}'
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_name}")
    tasks = cur.fetchall()

    if tasks:
        elements = ""
        for element in tasks:
            elements += f"🏷️{element[0]} | {element[2]} | {element[1]}\n"
        conn.commit()
        bot.send_message(call.message.chat.id, elements)
    else:
        bot.send_message(call.message.chat.id, "❌ You don't have any tasks.")

def choose_task(bot, call, user_name):
    bot_message = bot.send_message(call.message.chat.id, 'Enter task number 🔍')
    bot.register_next_step_handler(bot_message, lambda msg: remove_task(bot, msg, user_name))

def remove_task(bot, message, user_name):
    number = message.text
    table_name = f'tasks_{user_name}'
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {table_name} WHERE number = ?", (number,))
    conn.commit()
    bot.send_message(message.chat.id, 'Task removed!')
