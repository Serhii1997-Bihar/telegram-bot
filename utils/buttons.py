from telebot import types

def main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Tasks", "Football", "Scripts", "English", "Books", "Zina"]
    keyboard.add(*[types.KeyboardButton(btn) for btn in buttons])
    return keyboard

def scripts_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    button12 = types.InlineKeyboardButton("Docker", callback_data='docker')
    button13 = types.InlineKeyboardButton("Server", callback_data='server')
    button14 = types.InlineKeyboardButton("Mongo", callback_data='mongo')
    button15 = types.InlineKeyboardButton("Git", callback_data='git')
    button16 = types.InlineKeyboardButton("Firewall", callback_data='firewall')
    button17 = types.InlineKeyboardButton("Nginx", callback_data='nginx')
    button18 = types.InlineKeyboardButton("AWS", callback_data='aws')
    keyboard.add(button12, button13, button14, button15, button16, button17, button18)
    return keyboard

def signup_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("Sign Up")
    keyboard.add(button)
    return keyboard

def admin_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Users", "Access"]
    keyboard.add(*[types.KeyboardButton(btn) for btn in buttons])
    return keyboard

def tasks_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    button1 = types.InlineKeyboardButton("Create", callback_data='create_task')
    button2 = types.InlineKeyboardButton("Show", callback_data='show_tasks')
    button3 = types.InlineKeyboardButton("Remove", callback_data='choose_task')
    keyboard.add(button1, button2, button3)
    return keyboard

def documents_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    button4 = types.InlineKeyboardButton("Operational", callback_data='operational')
    button5 = types.InlineKeyboardButton("Documents", callback_data='documents')
    button6 = types.InlineKeyboardButton("Operator", callback_data='operator')
    keyboard.add(button4, button5, button6)
    return keyboard

def books_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    button10 = types.InlineKeyboardButton("Finished books", callback_data='read_books')
    button11 = types.InlineKeyboardButton("New books", callback_data='new_books')
    keyboard.add(button10, button11)
    return keyboard

def users_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    button1 = types.InlineKeyboardButton("Show", callback_data='show_users')
    button2 = types.InlineKeyboardButton("Remove", callback_data='remove_user')
    keyboard.add(button1, button2)
    return keyboard