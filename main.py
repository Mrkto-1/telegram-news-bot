import asyncio
import feedparser
from aiogram import Bot, Dispatcher, types
from datetime import datetime
import random

from config import BOT_TOKEN, CHANNEL_ID, RSS_FEEDS
from utils.filters import is_relevant
from utils.translator import translate_text

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
posted_links = set()
keywords_used_today = set()

# ключові слова
KEYWORDS = ["фрс", "ставка", "інфляція", "економіка", "криза", "рецесія", "s&p", "s & p"]
KEYWORDS_CRYPTO = ["криптовалюта", "біткоїн", "bitcoin", "ethereum", "crypto"]

# дозволено для старту
FIRST_RUN = True

def contains_keywords(text):
    text_lower = text.lower()
    if any(kw in text_lower for kw in KEYWORDS):
        return True
    if any(kw in text_lower for kw in KEYWORDS_CRYPTO) and ("крах" in text_lower or "регулювання" in text_lower or "заборона" in text_lower):
        return True
    return False

def extract_main_keyword(text):
    text_lower = text.lower()
    for kw in KEYWORDS + KEYWORDS_CRYPTO:
        if kw in text_lower:
            return kw
    return None

async def fetch_and_post():
    global FIRST_RUN
    while True:
        now = datetime.now()
        if not (6 <= now.hour or now.hour < 2):
            await asyncio.sleep(600)
            continue

        print("🔎 Перевірка новин...")

        found = 0
        for feed_url in RSS_FEEDS:
            if found >= (3 if FIRST_RUN else 1):
                break

            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                title = entry.title
                link = entry.link

                if link in posted_links:
                    continue

                if not contains_keywords(title):
                    continue

                main_kw = extract_main_keyword(title)
                if main_kw in keywords_used_today:
                    continue

                translated_title = translate_text(title)
                message = f"📉 <b>{translated_title}</b>\n🔗 <a href='{link}'>Читати повністю</a>"

                try:
                    await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode=types.ParseMode.HTML)
                    posted_links.add(link)
                    if main_kw:
                        keywords_used_today.add(main_kw)
                    found += 1
                    await asyncio.sleep(5)
                except Exception as e:
                    print(f"❌ Помилка надсилання: {e}")

                if found >= (3 if FIRST_RUN else 1):
                    break

        FIRST_RUN = False
        await asyncio.sleep(60 * 20)  # 20 хвилин


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_and_post())
