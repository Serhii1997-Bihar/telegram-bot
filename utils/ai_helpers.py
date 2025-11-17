from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
gpt_key = os.getenv('OPENAI_KEY')

client = OpenAI(api_key=gpt_key)
def ask_gpt(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150)
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error gpt-4o-mini: {str(e)}"