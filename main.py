import os
import asyncio
import feedparser
import sqlite3
from aiogram import Bot, Dispatcher
from datetime import datetime
from config import BOT_TOKEN, CHANNEL_ID, RSS_FEEDS, ACTIVE_HOURS, KEYWORDS, KEYWORDS_CRYPTO

# Ініціалізація Telegram-бота
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# Підключення до SQLite бази
conn = sqlite3.connect("posted_links.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS links (link TEXT PRIMARY KEY)")

def is_link_posted(link: str) -> bool:
    cursor.execute("SELECT 1 FROM links WHERE link=?", (link,))
    return cursor.fetchone() is not None

def mark_link_as_posted(link: str):
    cursor.execute("INSERT INTO links VALUES (?)", (link,))
    conn.commit()

def get_image(entry) -> str or None:
    for link in entry.get("links", []):
        if link.get("type", "").startswith("image"):
            return link.get("href")
    return None

def contains_keywords(text: str) -> bool:
    text = text.lower()
    return any(kw in text for kw in KEYWORDS + KEYWORDS_CRYPTO)

def format_post(title: str, summary: str) -> str:
    summary = summary.strip()
    return f"<b>{title}</b>\n\n{summary}\n\n#економіка"

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
                    print(f"❌ Помилка RSS: {feed_url} — {feed.bozo_exception}")
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
                    if not contains_keywords(title + summary):
                        continue

                    caption = format_post(title, summary)

                    try:
                        await bot.send_photo(
                            chat_id=CHANNEL_ID,
                            photo=image_url,
                            caption=caption[:1024]  # Telegram обмеження
                        )
                        mark_link_as_posted(link)
                        print(f"✅ Опубліковано: {title}")
                    except Exception as e:
                        print(f"🚫 Помилка публікації: {e}")

                    await asyncio.sleep(10)

            except Exception as e:
                print(f"⚠️ Помилка обробки джерела {feed_url}: {e}")

        await asyncio.sleep(1200)  # Перевірка кожні 20 хв

if __name__ == "__main__":
    try:
        asyncio.run(fetch_and_post())
    except KeyboardInterrupt:
        print("🛑 Бот зупинено вручну")
    finally:
        conn.close()
