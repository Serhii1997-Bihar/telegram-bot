from database.init_sqlite import get_db_connection
from utils.ai_helpers import ask_gpt
from dotenv import load_dotenv
import requests, os

load_dotenv()
weather_key = os.getenv('WEATHER_KEY')
def get_weather(bot):
    api_key = weather_key
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
                continue

            url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric&lang=en"
            response = requests.get(url)

            weather_data = response.json()
            temp = weather_data['main']['temp']
            description = weather_data['weather'][0]['description']
            for_ai = f"You are my funny morning assistant. Create a short funny sentence. Today {description} in {city_name}, {temp}°C."
            
            bot.send_message(user_id, ask_gpt(for_ai))

        except Exception as e:
            print(f"Error {user_name}: {e}")