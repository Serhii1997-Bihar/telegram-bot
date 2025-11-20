from database.init_sqlite import get_db_connection
import sqlite3

def new_books(bot, call, user_name):
    table_name = f'books_{user_name}'

    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} (number INTEGER PRIMARY KEY AUTOINCREMENT, "
            f"author TEXT NOT NULL, book TEXT NOT NULL)"
        )
        cur.execute(f"SELECT * FROM {table_name}")
        books = cur.fetchall()

    if books:
        elements = ""
        for element in books:
            elements += f"📖{element[0]} | {element[1]} - {element[2]}\n"
        bot.send_message(call.message.chat.id, '📚 These are your new books...')
        bot.send_message(call.message.chat.id, elements)

    bot_message = bot.send_message(call.message.chat.id, 'Add?')
    bot.register_next_step_handler(bot_message, lambda msg: add_newbook(bot, msg, user_name))


def add_newbook(bot, message, user_name):
    if message.text.lower() == 'yes':
        bot_message = bot.send_message(message.chat.id, 'Enter author, the title of book.')
        bot.register_next_step_handler(bot_message, lambda msg: add_new_to_db(bot, msg, user_name))
    else:
        bot.send_message(message.chat.id, 'Ok!')


def add_new_to_db(bot, message, user_name):
    try:
        book_data = message.text.split(",")
        if len(book_data) == 2:
            author = book_data[0].strip()
            book = book_data[1].strip()
            table_name = f'books_{user_name}'

            with get_db_connection() as conn:
                cur = conn.cursor()
                cur.execute(
                    f"INSERT INTO {table_name} (author, book) VALUES (?, ?)",
                    (author, book)
                )
                conn.commit()

            bot.send_message(message.chat.id, "Ok! The book added.")
        else:
            bot.send_message(message.chat.id, "Please enter the author and the book title, separated by a comma.")
            bot.register_next_step_handler(message, lambda msg: add_newbook(bot, msg, user_name))
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")


def read_books(bot, message, user_name):
    table_name = f'mybooks_{user_name}'

    with get_db_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                f"CREATE TABLE IF NOT EXISTS {table_name} (number INTEGER PRIMARY KEY AUTOINCREMENT, "
                f"author TEXT NOT NULL, book TEXT NOT NULL)"
            )
        except sqlite3.Error as e:
            bot.send_message(message.message.chat.id, f"Error: {e}")
            return

        cur.execute(f"SELECT * FROM {table_name}")
        books = cur.fetchall()

    if books:
        elements = ""
        for element in books:
            elements += f"📖{element[0]} | {element[1]} - {element[2]}\n"
        bot.send_message(message.message.chat.id, '📚 Your read books...')
        bot.send_message(message.message.chat.id, elements)
    else:
        bot.send_message(message.message.chat.id, "You don't have any finished books!")

    bot_message = bot.send_message(message.message.chat.id, 'Do you have a new finished book?')
    bot.register_next_step_handler(bot_message, lambda msg: add_read_book(bot, msg, user_name))


def add_read_book(bot, message, user_name):
    if message.text.lower() == 'yes':
        bot_message = bot.send_message(
            message.chat.id,
            'Enter the number of the book you have read, and I will add it to your read list.'
        )
        bot.register_next_step_handler(bot_message, lambda msg: add_read_to_db(bot, msg, user_name))
    else:
        bot.send_message(message.chat.id, 'Ok!')


def add_read_to_db(bot, message, user_name):
    number_book = message.text
    newbooks = f'books_{user_name}'
    mybooks = f'mybooks_{user_name}'

    with get_db_connection() as conn:
        cur = conn.cursor()

        cur.execute(f"SELECT * FROM {newbooks} WHERE number = ?", (number_book,))
        mybook = cur.fetchone()

        cur.execute(
            f"INSERT INTO {mybooks} (author, book) VALUES (?, ?)",
            (mybook[1], mybook[2])
        )
        cur.execute(f"DELETE FROM {newbooks} WHERE number = ?", (number_book,))
        conn.commit()

    bot.send_message(message.chat.id, 'Ok!')
    bot.send_message(message.chat.id, f"Beautiful book, '{mybook[2]}'")
