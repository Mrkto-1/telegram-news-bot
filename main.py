import os
import asyncio
import feedparser
import sqlite3
from aiogram import Bot, Dispatcher
from datetime import datetime
from config import BOT_TOKEN, CHANNEL_ID, RSS_FEEDS, ACTIVE_HOURS, KEYWORDS, KEYWORDS_CRYPTO
from utils.filters import is_blacklisted

# Ініціалізація бота
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# Підключення до бази даних для збереження унікальних посилань
conn = sqlite3.connect("posted_links.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS links (link TEXT PRIMARY KEY)")

# Перевірка чи лінк вже був
def is_link_posted(link):
    cursor.execute("SELECT 1 FROM links WHERE link=?", (link,))
    return cursor.fetchone() is not None

# Позначаємо лінк як опублікований
def mark_link_as_posted(link):
    cursor.execute("INSERT INTO links VALUES (?)", (link,))
    conn.commit()

# Витягуємо зображення з RSS
def get_image(entry):
    for link in entry.get("links", []):
        if link.get("type", "").startswith("image"):
            return link.get("href")
    return None

# Перевірка на ключові слова
def contains_keywords(text):
    text = text.lower()
    crypto_trigger = any(kw in text for kw in KEYWORDS_CRYPTO) and any(word in text for word in ["крах", "регулювання", "заборона"])
    return any(kw in text for kw in KEYWORDS) or crypto_trigger

# Формування посту
def format_post(title, summary):
    return f"<b>{title}</b>\n\n{summary.strip()}\n\n#економіка"[:1024]

# Основна логіка
async def fetch_and_post():
    while True:
        now = datetime.now()
        if not (ACTIVE_HOURS[0] <= now.hour < ACTIVE_HOURS[1]):
            await asyncio.sleep(600)
            continue

        for feed_url in RSS_FEEDS:
            try:
                feed = feedparser.parse(feed_url)
                if feed.get("bozo", False):
                    print(f"❌ RSS помилка: {feed_url} — {feed.bozo_exception}")
                    continue

                for entry in feed.entries:
                    link = entry.link
                    title = entry.title
                    summary = entry.get("summary", "")
                    image_url = get_image(entry)

                    if not image_url:
                        continue
                    if is_link_posted(link):
                        continue
                    if is_blacklisted(title + summary):
                        continue
                    if not contains_keywords(title + summary):
                        continue

                    caption = format_post(title, summary)

                    try:
                        await bot.send_photo(
                            chat_id=CHANNEL_ID,
                            photo=image_url,
                            caption=caption
                        )
                        mark_link_as_posted(link)
                        print(f"✅ Опубліковано: {title}")
                    except Exception as e:
                        print(f"⚠️ Помилка публікації: {e}")

                    await asyncio.sleep(10)

            except Exception as e:
                print(f"⚠️ Проблема з RSS {feed_url}: {e}")

        await asyncio.sleep(1200)  # 20 хв

# Запуск
if __name__ == "__main__":
    try:
        asyncio.run(fetch_and_post())
    except KeyboardInterrupt:
        print("⛔ Зупинено вручну")
    finally:
        conn.close()
