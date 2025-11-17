from bs4 import BeautifulSoup
import requests

def get_matches():
    url = "https://football.ua/scoreboard/"
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0"}

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    matches = soup.find_all('div', class_='match')

    if not matches:
        return 'There are not matches'

    result = ""
    for match in matches:
        time = match.find('td', class_='time')
        home = match.find('td', class_='left-team')
        score = match.find('td', class_='score')
        away = match.find('td', class_='right-team')

        if all([time, home, score, away]):
            result += f"{time.text.strip()} | {home.text.strip()} {score.text.strip()} {away.text.strip()}\n"
    
    return result