import telebot, sqlite3, schedule, requests, time, threading, datetime, pytz, wikipedia, os, random, translators as ts, html
from telebot import types
from bs4 import BeautifulSoup

bot = telebot.TeleBot("6025097478:AHyI7hFtYfQtDdkpJG8cECr74C0tH0-g")
ukr_time = pytz.timezone('Europe/Kiev')
serv_deii = "serv_deii"
chaude_neige = "Chaude_Neige"

current_directory = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_directory, 'JOHN NEGRETO.db')

def init_db():
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS employers (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                city TEXT NOT NULL,
                age INTEGER NOT NULL,
                phone TEXT NOT NULL
            )
        ''')
        conn.commit()

init_db()
def get_db_connection():
    conn = sqlite3.connect('JOHN NEGRETO.db', check_same_thread=False)
    return conn

def is_registered(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employers WHERE user_id = ?", (user_id,))
    return cur.fetchone() is not None

def water_reminder(chaude_neige):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM employers WHERE username = ?", (chaude_neige,))
    user = cur.fetchone()
    conn.close()
    if not user:
        return "User not found"
    user_id = user[0]
    bot.send_message(user_id, "Вам потрібно попити водички, або вінішка. Але краще воду, не забудьте!")

def water_planner():
    schedule.every().day.at("10:00").do(lambda: water_reminder(chaude_neige))
    schedule.every().day.at("13:00").do(lambda: water_reminder(chaude_neige))
    schedule.every().day.at("18:00").do(lambda: water_reminder(chaude_neige))

    while True:
        schedule.run_pending()
        time.sleep(60)

def english_reminder(serv_deii):
    try:
        api_key = "8iosekjr7jag8hbl3avi9tsyao26sp2m3ebp8z7stw2rdc5op"
        base_url = "https://api.wordnik.com/v4"

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT user_id FROM employers WHERE username = ?", (serv_deii,))
        user = cur.fetchone()
        conn.close()

        if not user:
            return "User not found"

        user_id = user[0]

        response = requests.get(f"{base_url}/words.json/randomWord", params={"api_key": api_key})
        if response.status_code != 200:
            return "Error fetching word from API"

        word = response.json().get("word")
        if not word or len(word) < 5:
            return "Word is too short or not received"

        response = requests.get(f"{base_url}/word.json/{word}/definitions", params={"api_key": api_key})
        definitions = response.json() if response.status_code == 200 else []
        if not definitions:
            return "No definitions found"

        word_type = definitions[0].get('partOfSpeech', '')
        if word_type not in ['noun', 'adjective', 'verb']:
            return "Selected word is not suitable"

        response = requests.get(f"{base_url}/word.json/{word}/examples", params={"api_key": api_key})
        examples = response.json().get("examples", []) if response.status_code == 200 else []
        if not examples or len(examples) < 5:
            return "Not enough examples for this word"

        sentence = examples[0].get("text", "No example found")
        translated_word = ts.translate_text(word, to_language='uk').lower()
        translated_sentence = ts.translate_text(sentence, to_language='uk')

        bot.send_message(user_id, f"<b>{html.escape(word)}</b> - <i>{html.escape(translated_word)}</i>\n\n"
                                  f"{html.escape(sentence)}\n\n"
                                  f"<i>{html.escape(translated_sentence)}</i>",
                         parse_mode="HTML")
    except Exception as e:
        return f"An error occurred: {e}"

def english_planner():
    schedule.every().day.at("12:30").do(lambda: english_reminder(serv_deii))

    while True:
        schedule.run_pending()
        time.sleep(60)

def message_reminder():
    API_KEY = 'b938e155c496afc5197c2923cc273eb1'
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employers")
    users = cur.fetchall()
    conn.close()
    for user in users:
        try:
            user_id = user[0]
            user_name = user[1]
            city_name = user[2]

            if not city_name:
                print(f"Пропущено користувача {user_name} без міста.")
                continue

            url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric&lang=en"
            response = requests.get(url)

            if response.status_code == 200:
                weather_data = response.json()
                temp = weather_data['main']['temp']
                description = weather_data['weather'][0]['description']
                bot.send_message(user_id, f"Good morning, {user_name}! Today {description} in {city_name}, "
                                          f"{temp}°C, make sure to dress appropriately for the weather..")
            else:
                print(f"Не вдалося отримати погоду для міста {city_name}")
                bot.send_message(user_id, f"Добрий ранок, {user_name}! Не вдалося отримати дані про погоду для міста {city_name}.")

        except Exception as e:
            print(f"Помилка при відправці повідомлення користувачу {user_name}: {e}")

def message_planner():
    schedule.every().day.at("06:00").do(message_reminder)
    while True:
        schedule.run_pending()
        time.sleep(60)

def task_reminder():
    now = datetime.datetime.now(ukr_time).strftime('%d-%m-%Y %H:%M')
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employers")
    users = cur.fetchall()
    for user in users:
        user_id = user[0]
        user_name = user[1]
        table_name = f'tasks_{user_name}'
        cur.execute(f"SELECT * FROM {table_name} WHERE date = ?", (now,))
        task = cur.fetchone()
        if task:
            bot.send_message(user_id, f'Не забудьте про {task[2]}')
            cur.execute(f"DELETE FROM {table_name} WHERE date = ?", (now,))
    conn.commit()
    conn.close()

def task_planner():
    schedule.every(1).minute.do(task_reminder)
    while True:
        schedule.run_pending()
        time.sleep(60)

@bot.message_handler(commands=["start"])
def registration(message):
    if is_registered(message.from_user.id):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Tasks")
        button2 = types.KeyboardButton("Football")
        button3 = types.KeyboardButton("Scripts")
        button4 = types.KeyboardButton("Zina")
        button5 = types.KeyboardButton("Books")
        button6 = types.KeyboardButton("Films")
        keyboard.add(button1, button2, button3, button6, button5, button4)
        bot.send_message(message.chat.id,
                         f"Can I help you, {message.from_user.first_name}?",
                         reply_markup=keyboard)
    else:
        starting = types.ReplyKeyboardMarkup(resize_keyboard=True)
        go = types.KeyboardButton("Sign Up")
        starting.add(go)
        bot_message = bot.send_message(message.chat.id, "Hello, I'm John Negreto."
                                                        "I can help you, but you need to sign up first.",
                                        reply_markup=starting)
        bot.register_next_step_handler_by_chat_id(message.chat.id, creation_1)

def creation_1(message):
    if message.text == "Sing Up":
        bot.send_message(message.chat.id, 'Which city do you live in?')
        bot.register_next_step_handler(message, creation_2)
    else:
        bot.send_message(message.chat.id, "Please, enter button 'Sign Up'")
        bot.register_next_step_handler(message, handle_registration)

def creation_2(message):
    user_city = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("Send my number", request_contact=True)
    keyboard.add(button)
    bot.send_message(message.chat.id, 'Enter your phone number by clicking the button.', reply_markup=keyboard)
    bot.register_next_step_handler_by_chat_id(message.chat.id, lambda msg: creation_3(msg, user_city))
def creation_3(message, user_city):
    if message.content_type == 'contact':
        user_number = message.contact.phone_number
        bot_message = bot.send_message(message.chat.id, 'How old are you?')
        bot.register_next_step_handler(bot_message, creation_over, user_city, user_number)
    else:
        bot.send_message(message.chat.id, 'Enter your phone number by clicking the button.')
        bot.register_next_step_handler(message, lambda msg: creation_3(msg, user_city))

def creation_over(message, user_city, user_number):
    user_age = message.text
    name_is = message.from_user.username
    if name_is:
        user_name = name_is
    else:
        rand_number = random.randint(1, 9999)
        user_name = f"user_N{rand_number}"
    user_id = message.from_user.id
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO employers (user_id, username, city, age, phone) VALUES (?, ?, ?, ?, ?)',
                    (user_id, user_name, user_city, user_age, user_number))
    conn.commit()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Tasks")
    button2 = types.KeyboardButton("Football")
    button3 = types.KeyboardButton("Scripts")
    button4 = types.KeyboardButton("Zina")
    button5 = types.KeyboardButton("Books")
    button6 = types.KeyboardButton("Films")
    keyboard.add(button1, button2, button3, button6, button5, button4)
    bot.send_message(message.chat.id, f"{user_name}, You are registered.", reply_markup=keyboard)

@bot.message_handler(func= lambda message: message.text == 'Tasks')
def tasks(message):
    if is_registered(message.from_user.id):
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Create", callback_data='button_1')
        button2 = types.InlineKeyboardButton("Show", callback_data='button_2')
        button3 = types.InlineKeyboardButton("Remove", callback_data='button_3')
        keyboard.add(button1, button2, button3)
        bot.send_message(message.chat.id, f"Choose a button", reply_markup=keyboard)
    else:
        starting = types.ReplyKeyboardMarkup(resize_keyboard=True)
        go = types.KeyboardButton("Sign Up")
        starting.add(go)
        bot.send_message(message.chat.id, "Please, enter button 'Sign Up'", reply_markup=starting)

@bot.message_handler(func=lambda message: message.text == 'Football')
def football(message):
    if not is_registered(message.from_user.id):
        bot.send_message(message.chat.id, "You need to register to use this feature.")
        return

    url = "https://football.ua/scoreboard/"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        bot.send_message(message.chat.id, f"Error: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    matches = soup.find_all('div', class_='match')

    if not matches:
        bot.send_message(message.chat.id, "No matches today.")
        return

    result = "Сьогоднішні матчі:\n\n"

    for match in matches:
        time = match.find('td', class_='time')
        home = match.find('td', class_='left-team')
        score = match.find('td', class_='score')
        away = match.find('td', class_='right-team')

        if all([time, home, score, away]):
            result += f"{time.text.strip()} | {home.text.strip()} {score.text.strip()} {away.text.strip()}\n"

    bot.send_message(message.chat.id, result)


@bot.message_handler(func=lambda message: message.text == 'Scripts')
def scripts(message):
    if is_registered(message.from_user.id):
        keyboard = types.InlineKeyboardMarkup(row_width=4)
        button12 = types.InlineKeyboardButton("Docker ", callback_data='button_12')
        button13 = types.InlineKeyboardButton("Server ", callback_data='button_13')
        button14 = types.InlineKeyboardButton("Mongo ", callback_data='button_14')
        button15 = types.InlineKeyboardButton("Git ", callback_data='button_15')
        keyboard.add(button12, button13, button14, button15)
        bot.send_message(message.chat.id, f"Choose a button", reply_markup=keyboard)
    else:
        starting = types.ReplyKeyboardMarkup(resize_keyboard=True)
        go = types.KeyboardButton("Sign Up")
        starting.add(go)
        bot.send_message(message.chat.id, "Please, enter button 'Sign Up'", reply_markup=starting)

@bot.message_handler(func=lambda message: message.text == 'Zina')
def work(message):
    if is_registered(message.from_user.id):
        keyboard = types.InlineKeyboardMarkup()
        button4 = types.InlineKeyboardButton("Operational", callback_data='button_4')
        button5 = types.InlineKeyboardButton("Documents", callback_data='button_5')
        button6 = types.InlineKeyboardButton("Videomanager", callback_data='button_6')
        keyboard.add(button4, button5, button6)
        bot.send_message(message.chat.id, f'{message.from_user.first_name}, can I help you?', reply_markup=keyboard)
    else:
        starting = types.ReplyKeyboardMarkup(resize_keyboard=True)
        go = types.KeyboardButton("Sign Up")
        starting.add(go)
        bot.send_message(message.chat.id, "Please, enter button 'Sign Up'", reply_markup=starting)

@bot.message_handler(func= lambda message: message.text == 'Films')
def films(message):
    if is_registered(message.from_user.id):
        keyboard = types.InlineKeyboardMarkup()
        button7 = types.InlineKeyboardButton("Add", callback_data='button_7')
        button8 = types.InlineKeyboardButton("Show", callback_data='button_8')
        button9 = types.InlineKeyboardButton("Remove", callback_data='button_9')
        keyboard.add(button7, button8, button9)
        bot.send_message(message.chat.id, f"Choose a button", reply_markup=keyboard)
    else:
        starting = types.ReplyKeyboardMarkup(resize_keyboard=True)
        go = types.KeyboardButton("Sign Up")
        starting.add(go)
        bot.send_message(message.chat.id, "Please, enter button 'Sign Up'", reply_markup=starting)

@bot.message_handler(func= lambda message: message.text == 'Books')
def books(message):
    if is_registered(message.from_user.id):
        keyboard = types.InlineKeyboardMarkup()
        button10 = types.InlineKeyboardButton("Finished books", callback_data='button_10')
        button11 = types.InlineKeyboardButton("New books", callback_data='button_11')
        keyboard.add(button10, button11)
        bot.send_message(message.chat.id, f"Choose a button", reply_markup=keyboard)
    else:
        starting = types.ReplyKeyboardMarkup(resize_keyboard=True)
        go = types.KeyboardButton("Sign Up")
        starting.add(go)
        bot.send_message(message.chat.id, "Please, enter button 'Sign Up'", reply_markup=starting)

@bot.callback_query_handler(func=lambda call: True)
def buttons_task(call):
    if call.message:
        user_name = call.from_user.username

        if call.data == "button_1":
            handle_task_creation(call, user_name)

        elif call.data == 'button_2':
            show_tasks(call, user_name)

        elif call.data == 'button_3':
            prompt_task_deletion(call, user_name)

        elif call.data == 'button_4':
            send_checklist(call)

        elif call.data == 'button_5':
            send_documents(call)

        elif call.data == 'button_6':
            send_google_drive_links(call)

        elif call.data == 'button_7':
            prompt_add_film(call, user_name)

        elif call.data == 'button_8':
            show_films(call)

        elif call.data == 'button_9':
            prompt_film_deletion(call, user_name)

        elif call.data == 'button_11':
            manage_books(call, user_name)

        elif call.data == 'button_10':
            my_books(call, user_name)

        elif call.data == 'button_13':
            server_notates(call, user_name)

        elif call.data == 'button_12':
            docker_notates(call, user_name)

        elif call.data == 'button_14':
            mongodb_notates(call, user_name)

        elif call.data == 'button_15':
            git_notates(call, user_name)

def handle_task_creation(call, user_name):
    table_name = f'tasks_{user_name}'
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (number INTEGER PRIMARY KEY AUTOINCREMENT, "
                f"date TEXT NOT NULL, task TEXT NOT NULL)")
    conn.commit()

    bot_message = bot.send_message(call.message.chat.id, 'Enter the date in the format DD-MM-YYYY HH:MM, and I will remind you about it.')
    bot.register_next_step_handler(bot_message, lambda msg: deadline(msg, table_name))

def deadline(message, table_name):
    deadline = message.text
    bot_message = bot.send_message(message.chat.id, 'Describe your task')
    bot.register_next_step_handler(bot_message, lambda msg: task_over(msg, deadline, table_name))

def task_over(message, deadline, table_name):
    task = message.text
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"INSERT INTO {table_name} (date, task) VALUES (?, ?)", (deadline, task))
    conn.commit()
    bot.send_message(message.chat.id, 'Task created!')

def show_tasks(call, user_name):
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
        bot.send_message(call.message.chat.id, f'Your tasks...')
        bot.send_message(call.message.chat.id, elements)
    else:
        bot.send_message(call.message.chat.id, "You don't have any tasks.")

def prompt_task_deletion(call, user_name):
    bot_message = bot.send_message(call.message.chat.id, 'Enter task number')
    bot.register_next_step_handler(bot_message, lambda msg: delete_task(msg, user_name))

def delete_task(message, user_name):
    number = message.text
    table_name = f'tasks_{user_name}'
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {table_name} WHERE number = ?", (number,))
    conn.commit()
    bot.send_message(message.chat.id, 'Task removed!')

def send_checklist(call):
    message_text = (
        "Чек-лист РЦ:\n"
        "https://docs.google.com/forms/d/e/1FAIpQLSeCUmyt0Xc4jHNJ9ez2gwLzobneIw2LibMJ4InTtJoC_Cc8hg/viewform\n\n"
        "Чек-лист магазину:\n"
        "https://forms.gle/QEEZLcPM9iJjb6Lp7\n"
        "https://docs.google.com/spreadsheets/d/181RYCpcl5_QKJ7WHyyjQ50ef_uJzU24P0IDC5ZbIYQg/edit#gid=2022098910\n\n"
        "Чек-лист менеджер:\n"
        "https://forms.gle/3JdwaWUnAPnQab849\n"
        "https://docs.google.com/spreadsheets/d/1zITMg2BaRNvXZpR0Q4dCp-tBSyXVCE-qGwR2rJfB5S8/edit?resourcekey#gid=1097342196\n\n"
        "Чек-лист менеджера Тімірязєва-12б:\n"
        "https://forms.gle/RuMnMbYJDE3JVpeb8\n"
        "https://docs.google.com/spreadsheets/d/1QZdLLkbhbhlYkeZ40yuCOz5UCTJ6l4QcbjgK2inD9c8/edit?resourcekey#gid=219982839\n\n"
        "Чек-лист магазину Тімірязєва-12б:\n"
        "https://forms.gle/r3fsLNMxmZYUaxY36\n"
        "https://docs.google.com/spreadsheets/d/1QZdLLkbhbhlYkeZ40yuCOz5UCTJ6l4QcbjgK2inD9c8/edit?resourcekey#gid=219982839\n\n"
        "Чек-лист пекарні:\n"
        "https://forms.gle/r3fsLNMxmZYUaxY36\n"
        "https://docs.google.com/spreadsheets/d/1QZdLLkbhbhlYkeZ40yuCOz5UCTJ6l4QcbjgK2inD9c8/edit?resourcekey#gid=219982839\n"
    )
    bot.send_message(call.message.chat.id, message_text)

def send_documents(call):
    file_1 = open('списання.xlsx', 'rb')
    file_2 = open('службова (дорога).docx', 'rb')
    file_3 = open('протерміновка.xlsx', 'rb')
    bot.send_document(call.message.chat.id, file_1)
    bot.send_document(call.message.chat.id, file_2)
    bot.send_document(call.message.chat.id, file_3)

def send_google_drive_links(call):
    message_text = (
        "Гугл диск СБ:\n"
        "https://drive.google.com/drive/my-drive\n\n"
        "Чек-лист магазину:\n"
        "https://docs.google.com/spreadsheets/d/17oXUoBVZ2YzGn9Urnb1S1zfKBP8ISt_tcBHCfAeBn_s/edit?gid=1262384048#gid=1262384048\n\n"
        "Зловживання працівників:\n"
        "https://docs.google.com/spreadsheets/d/13yAl_IVZ8EQmnH0QDUZhCAG4059_ntWCuqegP5EYNe4/edit#gid=1882209401\n\n"
        "Графіки роботи магазинів:\n"
        "https://drive.google.com/drive/folders/1-4XhgndS2oH_HDHc9UHF521raijsFnpE\n\n"
    )
    bot.send_message(call.message.chat.id, message_text)

def prompt_add_film(call, user_name):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS films (number INTEGER PRIMARY KEY AUTOINCREMENT, names TEXT NOT NULL)")
    conn.commit()
    bot_message = bot.send_message(call.message.chat.id,
                                   'If you find a good movie, let me know — I’ll remember it.')
    bot.register_next_step_handler(bot_message, lambda msg: films(msg, user_name))

def films(message, user_name):
    film = message.text
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO films (names) VALUES (?)", (film,))
    conn.commit()
    bot.send_message(message.chat.id, "Ok!")

def show_films(call):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM films")
    films = cur.fetchall()

    if films:
        elements = ""
        for element in films:
            elements += f"{element[0]}. {element[1]}\n"
        conn.commit()
        bot.send_message(call.message.chat.id, f'Your films for watching...')
        bot.send_message(call.message.chat.id, elements)
    else:
        bot.send_message(call.message.chat.id,
                         "You don't have any films")

def prompt_film_deletion(call, user_name):
    bot_message = bot.send_message(call.message.chat.id, 'Enter film number')
    bot.register_next_step_handler(bot_message, lambda msg: delete_film(msg, user_name))

def delete_film(message, user_name):
    number = message.text
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"DELETE FROM films WHERE number = ?", (number,))
    conn.commit()
    bot.send_message(message.chat.id, 'Film removed!')

def manage_books(call, user_name):
    table_name = f'books_{user_name}'
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (number INTEGER PRIMARY KEY AUTOINCREMENT, "
                f"author TEXT NOT NULL, book TEXT NOT NULL)")
    cur.execute(f"SELECT * FROM {table_name}")
    books = cur.fetchall()

    if books:
        elements = ""
        for element in books:
            elements += f"{element[0]}) {element[1]} - {element[2]}\n"
        conn.commit()
        bot.send_message(call.message.chat.id, f'These are your new books...')
        bot.send_message(call.message.chat.id, elements)

    # Пропонуємо користувачеві додати ще книги
    bot_message = bot.send_message(call.message.chat.id, f'Add?')
    bot.register_next_step_handler(bot_message, lambda msg: yes_or_no(msg, user_name))

def yes_or_no(message, user_name):
    if message.text.lower() == 'так' or message.text.lower() == 'да' or message.text.lower() == 'yes':
        bot_message = bot.send_message(message.chat.id, 'Enter author, the title of book.')
        bot.register_next_step_handler(bot_message, lambda msg: add_book(msg, user_name))
    else:
        bot.send_message(message.chat.id, 'Ok!')

def add_book(message, user_name):
    try:
        book_data = message.text.split(",")
        if len(book_data) == 2:
            author = book_data[0].strip()
            book = book_data[1].strip()
            table_name = f'books_{user_name}'
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(f"INSERT INTO {table_name} (author, book) VALUES (?, ?)", (author, book))
            conn.commit()
            bot.send_message(message.chat.id, "Ok! The book added.")
        else:
            bot.send_message(message.chat.id,
                             "Please enter the author and the book title, separated by a comma.")
            bot.register_next_step_handler(message, lambda msg: add_book(msg, user_name))
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

def my_books(message, user_name):
    table_name = f'mybooks_{user_name}'
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (number INTEGER PRIMARY KEY AUTOINCREMENT, "
                    f"author TEXT NOT NULL, book TEXT NOT NULL)")
    except sqlite3.Error as e:
        bot.send_message(message.message.chat.id, f"Error: {e}")
        return
    cur.execute(f"SELECT * FROM {table_name}")
    books = cur.fetchall()
    if books:
        elements = ""
        for element in books:
            elements += f"{element[0]}) {element[1]} - {element[2]}\n"
        bot.send_message(message.message.chat.id, 'Your books...')
        bot.send_message(message.message.chat.id, elements)
    else:
        bot.send_message(message.message.chat.id, "You don't have any finished books!")
    bot_message = bot.send_message(message.message.chat.id, 'Do you have a new finished book?')
    bot.register_next_step_handler(bot_message, lambda msg: yes_or_no2(msg, user_name))

def yes_or_no2(message, user_name):
    if message.text.lower() == 'так' or message.text.lower() == 'да':
        bot_message = bot.send_message(message.chat.id, 'Enter the number of the book you have read, and I will add it to your read list.')
        bot.register_next_step_handler(bot_message, lambda msg: add_mybook(msg, user_name))
    else:
        bot.send_message(message.chat.id, 'Ok!')

def add_mybook(message, user_name):
    number_book = message.text
    newbooks = f'books_{user_name}'
    mybooks = f'mybooks_{user_name}'
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {newbooks} WHERE number = ?", (number_book,))
    mybook = cur.fetchone()
    cur.execute(f"INSERT INTO {mybooks} (author, book) VALUES (?, ?)", (mybook[1], mybook[2]))
    cur.execute(f"DELETE FROM {newbooks} WHERE number = ?", (number_book,))
    conn.commit()
    bot.send_message(message.chat.id, 'Ok!')
    bot.send_message(message.chat.id, f"Beautiful book, '{mybook[2]}'")

def server_notates(call, username):
    notate = (
        "<code>|nohup python manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &</code>\n"
        "<code>|ps aux | grep manage.py runserver</code>\n"
        "<code>|tail -n 20 server.log</code>\n"
        "<code>|pkill -f \"manage.py runserver\"</code>\n"
        "<code>|scp -r C:\PyCharm\work_projects\18.03.2025\pricesua_project\pricesua_project root@116.203.238.17:/root/price/</code>\n"
        "<code>|kill 2554458</code>\n"
        "<code>|pip install -r requirements.txt</code>\n"
        "<code>|scp -r user@host:/remote/folder ./local</code>\n"
        "<code>|apt update && apt install -y postgresql ...</code>\n"
        "<code>|sudo -u postgres psql</code>")
    bot.send_message(call.message.chat.id, f"<pre>{notate}</pre>", parse_mode='HTML')

def docker_notates(call, username):
    commands = (
        "<code>|docker build -t myimage .</code>\n"
        "<code>|docker run -d -p 8000:8000 myimage</code>\n"
        "<code>|docker ps</code>\n"
        "<code>|docker ps -a</code>\n"
        "<code>|docker stop &lt;container_id&gt;</code>\n"
        "<code>|docker rm &lt;container_id&gt;</code>\n"
        "<code>|docker rmi &lt;image_id&gt;</code>\n"
        "<code>|docker logs &lt;container_id&gt;</code>\n"
        "<code>|docker exec -it &lt;container_id&gt; /bin/bash</code>\n"
        "<code>|docker-compose up -d</code>\n"
        "<code>|docker-compose down</code>")

    docker = (
        "<pre><code class=\"language-dockerfile\">"
        "FROM python:3.10-slim\n"
        "WORKDIR /app\n"
        "COPY . /app\n"
        "RUN pip install --no-cache-dir -r requirements.txt\n"
        "EXPOSE 8000\n"
        "CMD [\"python\", \"manage.py\", \"runserver\", \"0.0.0.0:8000\"]"
        "</code></pre>\n"
        "<pre><code class=\"language-yaml\">"
        "version: '3.8'\n"
        "services:\n"
        "  web:\n"
        "    build: .\n"
        "    ports:\n"
        "      - \"8000:8000\"\n"
        "    volumes:\n"
        "      - .:/app\n"
        "    command: python manage.py runserver 0.0.0.0:8000\n"
        "  db:\n"
        "    image: postgres:13\n"
        "    environment:\n"
        "      POSTGRES_USER: user\n"
        "      POSTGRES_PASSWORD: password\n"
        "      POSTGRES_DB: mydb\n"
        "    ports:\n"
        "      - \"5432:5432\"\n"
        "    volumes:\n"
        "      - pgdata:/var/lib/postgresql/data\n"
        "volumes:\n"
        "  pgdata:"
        "</code></pre>")

    bot.send_message(call.message.chat.id, f"<pre>{commands}</pre>", parse_mode='HTML')
    bot.send_message(call.message.chat.id, docker, parse_mode='HTML')

def mongodb_notates(call, username):
    commands = (
        "<code>|sudo apt install -y mongodb</code>\n"
        "<code>|sudo systemctl start mongodb</code>\n"
        "<code>|sudo systemctl status mongodb</code>\n"
        "<code>|sudo systemctl enable mongodb</code>\n"
        "<code>|mongo</code>\n"
        "<code>|mongo --host 127.0.0.1 --port 27017</code>\n"
        "<code>|mongodump --db=test --out=/backup/test</code>\n"
        "<code>|mongorestore --db=test /backup/test</code>\n"
        "<code>|sudo service mongod restart</code>\n"
        "<code>|sudo service mongod stop</code>\n"
        "<code>|sudo service mongod start</code>\n"
        "<code>|use mydatabase</code>\n"
        "<code>|db.mycollection.insertOne({name: \"Serhii\", age: 28})</code>\n"
        "<code>|db.mycollection.find()</code>\n"
        "<code>|db.mycollection.updateOne({name: \"Serhii\"}, {$set: {age: 29}})</code>\n"
        "<code>|db.mycollection.deleteOne({name: \"Serhii\"})</code>\n"
        "<code>|show dbs</code>\n"
        "<code>|show collections</code>\n")
    bot.send_message(call.message.chat.id, f"<pre>{commands}</pre>", parse_mode='HTML')

def git_notates(call, username):
    commands = (
        "<code>|git init</code>\n"
        "<code>|git clone https://github.com/user/repo.git</code>\n"
        "<code>|git status</code>\n"
        "<code>|git add .</code>\n"
        "<code>|git commit -m \"Initial commit\"</code>\n"
        "<code>|git push origin main</code>\n"
        "<code>|git pull origin main</code>\n"
        "<code>|git branch</code>\n"
        "<code>|git checkout -b new-branch</code>\n"
        "<code>|git checkout main</code>\n"
        "<code>|git merge new-branch</code>\n"
        "<code>|git log</code>\n"
        "<code>|git remote -v</code>\n"
        "<code>|git stash</code>\n"
        "<code>|git stash apply</code>\n"
        "<code>|git reset --hard</code>\n"
        "<code>|git config --global user.name \"Your Name\"</code>\n"
        "<code>|git config --global user.email \"your.email@example.com\"</code>\n"
    )
    bot.send_message(call.message.chat.id, f"<pre>{commands}</pre>", parse_mode='HTML')







if __name__ == "__main__":
    threading.Thread(target=task_planner, daemon=True).start()
    threading.Thread(target=message_planner, daemon=True).start()
    threading.Thread(target=english_planner, daemon=True).start()
    threading.Thread(target=water_planner, daemon=True).start()
    bot.polling(none_stop=True)
