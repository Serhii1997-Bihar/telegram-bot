import telebot, schedule, time, threading
from features.voc.vocabulary import get_dictionary
from features.english import english_reminder
from features.reminders.weather import get_weather
from features.reminders.task_reminder import task_reminder
from features.sport import get_matches
from utils.authenticate import is_registered, is_admin
from database.init_sqlite import init_db
from utils.authorise import get_city
from features.admin import get_users, choose_user
from utils.buttons import *
from features.tasks import *
from features.zina import *
from features.books import *
from features.scripts import *
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

init_db()

def english_planner():
    times = ["07:33", "08:41", "09:05", "10:46", "11:25", "13:46", "14:41", "16:48", "17:21","18:33"]
    
    for t in times:
        schedule.every().day.at(t).do(lambda: english_reminder(bot))

    while True:
        schedule.run_pending()
        time.sleep(60)

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

@bot.message_handler(commands=["admin"])
def admin(message):
    if is_admin(message.from_user.id):
        bot.send_message(message.chat.id,f"Hello admin!", reply_markup=admin_keyboard())
    else:
        bot.send_message(message.chat.id,"You don't have admin access!")
        
@bot.message_handler(func= lambda message: message.text == 'Tasks')
def tasks(message):
    if is_registered(message.from_user.id):
        bot.send_message(message.chat.id, f"Choose a button ☑️", reply_markup=tasks_keyboard())
    else:
        bot.send_message(message.chat.id, "Please, enter button 'Sign Up'", reply_markup=signup_keyboard())

@bot.message_handler(func=lambda message: message.text == 'Football')
def football(message):
    if is_registered(message.from_user.id):
        bot.send_message(message.chat.id, get_matches())
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
        bot.send_message(message.chat.id, f'{message.from_user.first_name}, can I help you?', reply_markup=documents_keyboard())
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
        bot.send_message(message.chat.id, f"Choose a button ☑️", reply_markup=books_keyboard())
    else:
        bot.send_message(message.chat.id, "Please, enter button 'Sign Up'", reply_markup=signup_keyboard())

@bot.message_handler(func= lambda message: message.text == 'Users')
def users(message):
    if is_admin(message.from_user.id):
        bot.send_message(message.chat.id, f"Choose a button ☑️", reply_markup=users_keyboard())
    else:
        bot.send_message(message.chat.id, "You don't have admin access!")

@bot.callback_query_handler(func=lambda call: True)
def buttons_task(call):
    if not call.message:
        return

    user_name = call.from_user.username
    actions = {
        'create_task': lambda: create_task(bot, call, call.from_user.id),
        'show_tasks': lambda: show_tasks(bot, call, call.from_user.id),
        'choose_task': lambda: choose_task(bot, call, user_name),
        'operational': lambda: get_operational(call, bot),
        'documents': lambda: get_documents(call, bot),
        'operator': lambda: get_operator(call, bot),
        'new_books': lambda: new_books(bot, call, call.from_user.id),
        'read_books': lambda: read_books(bot, call, call.from_user.id),
        'server': lambda: server(bot, call),
        'docker': lambda: docker(bot, call),
        'mongo': lambda: mongodb(bot, call),
        'git': lambda: git(bot, call),
        'firewall': lambda: firewall(bot, call),
        'nginx': lambda: nginx(bot, call),
        'show_users': lambda: get_users(bot, call),
        'remove_user': lambda: choose_user(bot, call) 
    }

    action = actions.get(call.data)
    if action:
        action()




if __name__ == "__main__":
    threading.Thread(target=task_planner, daemon=True).start()
    threading.Thread(target=weather_planner, daemon=True).start()
    threading.Thread(target=english_planner, daemon=True).start()
    bot.polling(none_stop=True)
