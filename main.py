import os
import asyncio
import feedparser
import sqlite3
from aiogram import Bot, Dispatcher
from aiogram.types import InputMediaPhoto
from datetime import datetime
from utils.filters import is_relevant
from utils.translator import translate_text

# Налаштування
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Джерела RSS
RSS_FEEDS = [
    "https://www.epravda.com.ua/rss/",
    "https://www.ukrinform.ua/rss/economics",
    "https://biz.liga.net/ekonomika/rss.xml",
    "https://mind.ua/rss/news",
    "https://forbes.ua/rss"
]

# Час активності бота (з 6:00 до 23:00)
ACTIVE_HOURS = (6, 23)

# Ключові слова для фільтрації
KEYWORDS = ["фрс", "ставка", "інфляція", "економіка", "криза", "рецесія", "s&p", "s & p"]
KEYWORDS_CRYPTO = ["криптовалюта", "біткоїн", "bitcoin", "ethereum", "crypto"]

# Ініціалізація бота
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# Ініціалізація бази даних для зберігання опублікованих посилань
conn = sqlite3.connect("posted_links.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS links (link TEXT PRIMARY KEY)")

def is_link_posted(link):
    """Перевіряє, чи посилання вже було опубліковане"""
    cursor.execute("SELECT 1 FROM links WHERE link=?", (link,))
    return cursor.fetchone() is not None

def mark_link_as_posted(link):
    """Позначає посилання як опубліковане"""
    cursor.execute("INSERT INTO links VALUES (?)", (link,))
    conn.commit()

def contains_keywords(text):
    """Перевіряє наявність ключових слів у тексті"""
    text = text.lower()
    return any(kw in text for kw in KEYWORDS + KEYWORDS_CRYPTO)

def get_image(entry):
    """Отримує URL зображення з RSS-запису"""
    for link in entry.get("links", []):
        if link.get("type", "").startswith("image"):
            return link.get("href")
    return None

def format_text(title, summary):
    """Форматує текст для публікації"""
    text = f"📰 <b>{title}</b>\n\n{summary}\n\n#Новини #Економіка"
    return text[:1000] + "..." if len(text) > 1000 else text

async def fetch_and_post():
    """Основна функція для отримання та публікації новин"""
    while True:
        now = datetime.now()
        
        # Перевірка часу активності
        if not (ACTIVE_HOURS[0] <= now.hour < ACTIVE_HOURS[1]):
            await asyncio.sleep(600)
            continue

        for feed_url in RSS_FEEDS:
            try:
                # Парсинг RSS
                feed = feedparser.parse(feed_url)
                if feed.get("bozo", False):
                    print(f"Помилка RSS: {feed_url} - {feed.bozo_exception}")
                    continue

                for entry in feed.entries:
                    link = entry.link
                    title = entry.title
                    summary = entry.get("summary", "")
                    image_url = get_image(entry)

                    # Перевірки перед публікацією
                    if not image_url:
                        continue
                    if is_link_posted(link):
                        continue
                    if not contains_keywords(title + summary):
                        continue

                    # Форматування тексту
                    text = format_text(title, summary)

                    # Спроба публікації
                    try:
                        await bot.send_photo(
                            CHANNEL_ID,
                            photo=image_url,
                            caption=text,
                            parse_mode="HTML"
                        )
                        mark_link_as_posted(link)
                        print(f"Опубліковано: {title}")
                    except Exception as e:
                        print(f"Помилка публікації: {e}")

                    # Пауза між публікаціями
                    await asyncio.sleep(10)

            except Exception as e:
                print(f"Помилка обробки RSS: {feed_url} - {e}")

        # Пауза між перевірками джерел
        await asyncio.sleep(1200)  # 20 хвилин

if __name__ == "__main__":
    try:
        asyncio.run(fetch_and_post())
    except KeyboardInterrupt:
        print("Бот зупинено")
    finally:
        conn.close()
