from contextlib import closing
from database.init_sqlite import get_db_connection
from features.voc.vocabulary import get_word
from utils.ai_helpers import ask_gpt

def english_reminder(bot):
    eng_1, ukr_1 = get_word()
    eng_2, ukr_2 = get_word()
    eng_3, ukr_3 = get_word()
    eng_4, ukr_4 = get_word()
    eng_5, ukr_5 = get_word()

    gpt_prompt = f"Just create one a good English sentence (A2-B1 level) using these words: {eng_1}, {eng_2}, {eng_3}, {eng_4}, {eng_5}."
    gpt_answer = ask_gpt(gpt_prompt)

    with get_db_connection() as conn:
        with closing(conn.cursor()) as cur:
            cur.execute("SELECT user_id FROM employers")
            users = cur.fetchall()

    for user in users:
        user_id = user[0]
        try:
            bot.send_message(user_id, gpt_answer, parse_mode="HTML")
        except Exception as e:
            print(f"❌ Failed to send message to {user_id}: {e}")
