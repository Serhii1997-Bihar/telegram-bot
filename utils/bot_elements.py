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