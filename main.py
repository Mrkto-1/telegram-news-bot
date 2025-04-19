import asyncio
import feedparser
from aiogram import Bot, Dispatcher, types
from datetime import datetime
import random

from config import BOT_TOKEN, CHANNEL_ID, RSS_FEEDS
from utils.translator import translate_text

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
posted_links = set()

FIRST_RUN = True  # одразу 3 новини

def extract_main_keyword(text):
    text_lower = text.lower()
    keywords = [
        "фрс", "ставка", "інфляція", "економіка",
        "криза", "рецесія", "s&p", "s & p",
        "криптовалюта", "біткоїн", "bitcoin", "ethereum", "crypto"
    ]
    for kw in keywords:
        if kw in text_lower:
            return kw
    return None

def get_emoji(keyword):
    emoji_map = {
        "фрс": "🏦",
        "ставка": "🏦",
        "інфляція": "📈",
        "криза": "💥",
        "рецесія": "💥",
        "економіка": "🌍",
        "s&p": "📉",
        "s & p": "📉",
        "криптовалюта": "🪙",
        "bitcoin": "🪙",
        "ethereum": "🪙",
        "crypto": "🪙",
    }
    return emoji_map.get(keyword, "🗞️")

def get_hashtags(keyword):
    tags_map = {
        "фрс": "#фрс #центробанк",
        "ставка": "#ставка #монетарнаполітика",
        "інфляція": "#інфляція #ціни",
        "криза": "#криза #спад",
        "рецесія": "#рецесія #економіка",
        "економіка": "#економіка",
        "s&p": "#ринок #акції",
        "s & p": "#ринок #акції",
        "криптовалюта": "#крипта #bitcoin",
        "bitcoin": "#bitcoin #btc",
        "ethereum": "#ethereum #eth",
        "crypto": "#crypto #altcoin",
    }
    return tags_map.get(keyword, "")

async def fetch_and_post():
    global FIRST_RUN
    while True:
        now = datetime.now()
        if not (6 <= now.hour < 24 or now.hour < 2):  # час 06:00 – 02:00
            print("⏸ За межами активного часу")
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
                    print(f"🔁 Пропущено: {title} (вже постили)")
                    continue

                is_ukrainian = any(src in feed_url for src in [
                    "epravda", "ukrinform", "liga.net", "mind.ua", "forbes.ua"
                ])
                translated_title = title if is_ukrainian else translate_text(title)

                main_kw = extract_main_keyword(title)
                emoji = get_emoji(main_kw)
                hashtags = get_hashtags(main_kw)

                message = f"{emoji} <b>{translated_title}</b>\n\n{hashtags}\n🔗 <a href='{link}'>Читати повністю</a>"

                try:
                    await bot.send_message(
                        chat_id=CHANNEL_ID,
                        text=message,
                        parse_mode=types.ParseMode.HTML
                    )
                    print(f
