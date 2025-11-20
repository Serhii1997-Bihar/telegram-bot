from database.init_sqlite import get_db_connection
import sqlite3

def new_books(bot, call, user_id):
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT book_id, author, book FROM books WHERE user_id = ?", (user_id,))
        books = cur.fetchall()

    if books:
        elements = ""
        for element in books:
            elements += f"📖{element[0]} | {element[1]} - {element[2]}\n"
        bot.send_message(call.message.chat.id, '📚 These are your new books...')
        bot.send_message(call.message.chat.id, elements)

    bot_message = bot.send_message(call.message.chat.id, 'Add?')
    bot.register_next_step_handler(bot_message, lambda msg: add_newbook(bot, msg, user_id))

def add_newbook(bot, message, user_id):
    if message.text.lower() == 'yes':
        bot_message = bot.send_message(message.chat.id, 'Enter author, the title of book.')
        bot.register_next_step_handler(bot_message, lambda msg: add_new_to_db(bot, msg, user_id))
    else:
        bot.send_message(message.chat.id, 'Ok!')

def add_new_to_db(bot, message, user_id):
    try:
        book_data = message.text.split(",")
        if len(book_data) == 2:
            author = book_data[0].strip()
            book = book_data[1].strip()

            with get_db_connection() as conn:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO books (user_id, author, book) VALUES (?, ?, ?)",
                    (user_id, author, book)
                )
                conn.commit()

            bot.send_message(message.chat.id, "Ok! The book added.")
        else:
            bot.send_message(message.chat.id, "Please enter the author and the book title, separated by a comma.")
            bot.register_next_step_handler(message, lambda msg: add_newbook(bot, msg, user_id))
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

def read_books(bot, message, user_id):
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT read_book_id, author, book FROM read_books WHERE user_id = ?", (user_id,))
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
    bot.register_next_step_handler(bot_message, lambda msg: add_read_book(bot, msg, user_id))

def add_read_book(bot, message, user_id):
    if message.text.lower() == 'yes':
        bot_message = bot.send_message(
            message.chat.id,
            'Enter the number of the book you have read, and I will add it to your read list.'
        )
        bot.register_next_step_handler(bot_message, lambda msg: add_read_to_db(bot, msg, user_id))
    else:
        bot.send_message(message.chat.id, 'Ok!')

def add_read_to_db(bot, message, user_id):
    book_id = message.text
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT author, book FROM books WHERE book_id = ? AND user_id = ?", (book_id, user_id))
        book = cur.fetchone()

        if book:
            cur.execute("INSERT INTO read_books (user_id, author, book) VALUES (?, ?, ?)", (user_id, book[0], book[1]))
            cur.execute("DELETE FROM books WHERE book_id = ? AND user_id = ?", (book_id, user_id))
            conn.commit()
            bot.send_message(message.chat.id, 'Ok!')
            bot.send_message(message.chat.id, f"Beautiful book, '{book[1]}'")
        else:
            bot.send_message(message.chat.id, "Book not found or does not belong to you.")
