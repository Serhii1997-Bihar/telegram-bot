import telebot, schedule, time, threading, os
from features.voc.vocabulary import get_dictionary
from features.english_feature import english_reminder
from features.reminders.weather_feature import get_weather
from features.reminders.tasks import task_reminder
from features.sport_feature import get_matches
from utils.authenticate import is_registered
from utils.bot_elements import main_keyboard, scripts_keyboard, signup_keyboard
from database.init_sqlite import init_db
from utils.authorise import get_city
from features.tasks_feature import *
from features.zina_feature import *
from features.books_feature import *
from features.scripts_feature import *
from dotenv import load_dotenv
from telebot import types

load_dotenv()
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

init_db()

def english_planner():
    times = ["07:33", "08:41", "09:05", "10:46", "11:25", "13:46", "14:41", "16:48", "17:21","18:33"]
    
    for t in times:
        schedule.every().day.at(t).do(lambda: english_reminder(bot))

    while True:
        schedule.run_pending()
        time.sleep(55)

def weather_planner():
    schedule.every().day.at("07:00").do(lambda: get_weather(bot))
    while True:
        schedule.run_pending()
        time.sleep(60)

def task_planner():
    schedule.every(1).minute.do(lambda: task_reminder(bot))
    while True:
        schedule.run_pending()
        time.sleep(60)

@bot.message_handler(commands=["start"])
def registration(message):
    if is_registered(message.from_user.id):
        bot.send_message(message.chat.id,f"Can I help you, {message.from_user.first_name}?", reply_markup=main_keyboard())
    else:
        bot.send_message(message.chat.id,"Hello, I'm Joopee Kipers. I can help you, but you need to sign up first.", reply_markup=signup_keyboard())
        bot.register_next_step_handler_by_chat_id(message.chat.id, lambda msg: get_city(bot, msg))

@bot.message_handler(func= lambda message: message.text == 'Tasks')
def tasks(message):
    if is_registered(message.from_user.id):
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Create", callback_data='create_task')
        button2 = types.InlineKeyboardButton("Show", callback_data='show_tasks')
        button3 = types.InlineKeyboardButton("Remove", callback_data='choose_task')
        keyboard.add(button1, button2, button3)
        bot.send_message(message.chat.id, f"Choose a button ☑️", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Please, enter button 'Sign Up'", reply_markup=signup_keyboard())

@bot.message_handler(func=lambda message: message.text == 'Football')
def football(message):
    if is_registered(message.from_user.id):
        matches = get_matches()
        bot.send_message(message.chat.id, matches)
    else:
        bot.send_message(message.chat.id, "Please, enter button 'Sign Up'", reply_markup=signup_keyboard())

@bot.message_handler(func=lambda message: message.text == 'Scripts')
def scripts(message):
    if is_registered(message.from_user.id):
        bot.send_message(message.chat.id, f"Choose a button ☑️", reply_markup=scripts_keyboard())
    else:
        bot.send_message(message.chat.id, "Please, enter button 'Sign Up'", reply_markup=signup_keyboard())

@bot.message_handler(func=lambda message: message.text == 'Zina')
def work(message):
    if is_registered(message.from_user.id):
        keyboard = types.InlineKeyboardMarkup()
        button4 = types.InlineKeyboardButton("Operational", callback_data='operational')
        button5 = types.InlineKeyboardButton("Documents", callback_data='documents')
        button6 = types.InlineKeyboardButton("Operator", callback_data='operator')
        keyboard.add(button4, button5, button6)
        bot.send_message(message.chat.id, f'{message.from_user.first_name}, can I help you?', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Please, enter button 'Sign Up'", reply_markup=signup_keyboard())

@bot.message_handler(func=lambda message: message.text == 'English')
def education(message):
    if is_registered(message.from_user.id):
        question = bot.send_message(message.chat.id, "What number of vocabulary do you want?")
        bot.register_next_step_handler(question, lambda msg: get_dictionary(bot, msg))
    else:
        bot.send_message(message.chat.id, "Please, enter button 'Sign Up'", reply_markup=signup_keyboard())

@bot.message_handler(func= lambda message: message.text == 'Books')
def books(message):
    if is_registered(message.from_user.id):
        keyboard = types.InlineKeyboardMarkup()
        button10 = types.InlineKeyboardButton("Finished books", callback_data='read_books')
        button11 = types.InlineKeyboardButton("New books", callback_data='new_books')
        keyboard.add(button10, button11)
        bot.send_message(message.chat.id, f"Choose a button ☑️", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Please, enter button 'Sign Up'", reply_markup=signup_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def buttons_task(call):
    if call.message:
        user_name = call.from_user.username

        if call.data == "create_task":
            create_task(bot, call, user_name)

        elif call.data == 'show_tasks':
            show_tasks(bot, call, user_name)

        elif call.data == 'choose_task':
            choose_task(bot, call, user_name)

        elif call.data == 'operational':
            get_operational(call, bot)

        elif call.data == 'documents':
            get_documents(call, bot)

        elif call.data == 'operator':
            get_operator(call, bot)

        elif call.data == 'new_books':
            new_books(bot, call, user_name)

        elif call.data == 'read_books':
            read_books(bot, call, user_name)

        elif call.data == 'server':
            server(bot, call)

        elif call.data == 'docker':
            docker(bot, call)

        elif call.data == 'mongo':
            mongodb(bot, call)

        elif call.data == 'git':
            git(bot, call)

        elif call.data == 'firewall':
            firewall(bot, call)

        elif call.data == 'nginx':
            nginx(bot, call)
            
        elif call.data == 'button_8':
            get_weather(bot)


if __name__ == "__main__":
    threading.Thread(target=task_planner, daemon=True).start()
    threading.Thread(target=weather_planner, daemon=True).start()
    threading.Thread(target=english_planner, daemon=True).start()
    bot.polling(none_stop=True)
