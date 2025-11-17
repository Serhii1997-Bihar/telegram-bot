from database.init_sqlite import get_db_connection
from utils.bot_elements import main_keyboard
import random
from telebot import types

def get_city(bot, message):
    if message.text == "Sign Up":
        bot.send_message(message.chat.id, 'Which city do you live in?')
        bot.register_next_step_handler(message, lambda msg: get_number(bot, msg))
    else:
        bot.send_message(message.chat.id, "Please, enter button 'Sign Up'")
        bot.register_next_step_handler(message, lambda msg: get_city(bot, msg))

def get_number(bot, message):
    user_city = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("Send my number", request_contact=True)
    keyboard.add(button)
    bot.send_message(message.chat.id, 'Enter your phone number by clicking the button.', reply_markup=keyboard)
    bot.register_next_step_handler_by_chat_id(message.chat.id, lambda msg: get_age(bot, msg, user_city))

def get_age(bot, message, user_city):
    if message.content_type == 'contact':
        user_number = message.contact.phone_number
        bot_message = bot.send_message(message.chat.id, 'How old are you?')
        bot.register_next_step_handler(bot_message, lambda msg: create_user(bot, msg, user_city, user_number))
    else:
        bot.send_message(message.chat.id, 'Enter your phone number by clicking the button.')
        bot.register_next_step_handler(message, lambda msg: get_age(bot, msg, user_city))

def create_user(bot, message, user_city, user_number):
    user_age = message.text
    user_name = message.from_user.username or f"user_N{random.randint(1,9999)}"
    user_id = message.from_user.id

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO employers (user_id, username, city, age, phone) VALUES (?, ?, ?, ?, ?)',
                (user_id, user_name, user_city, user_age, user_number))
    conn.commit()
    bot.send_message(message.chat.id, f"{user_name}, You are registered.", reply_markup=main_keyboard())
