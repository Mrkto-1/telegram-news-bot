import os
import asyncio
import feedparser
import sqlite3
from aiogram import Bot, Dispatcher
from datetime import datetime
from utils.filters import is_blacklisted

# === Налаштування ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

if not BOT_TOKEN or not CHANNEL_ID:
    raise ValueError("❌ BOT_TOKEN або CHANNEL_ID не встановлено!")

# RSS-джерела (українські)
RSS_FEEDS = [
    "https://www.epravda.com.ua/rss/",
    "https://www.ukrinform.ua/rss/economics",
    "https://biz.liga.net/ekonomika/rss.xml",
    "https://mind.ua/rss/news",
    "https://forbes.ua/rss"
]

# Ключові слова (дозволені теми)
KEYWORDS = ["фрс", "ставка", "інфляція", "економіка", "криза", "рецесія", "s&p", "s & p"]
KEYWORDS_CRYPTO = ["криптовалюта", "біткоїн", "bitcoin", "ethereum", "crypto"]

# Години активності (6:00 — 23:00)
ACTIVE_HOURS = (6, 23)

# Ініціалізація бота
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# База даних для перевірки дублів
conn = sqlite3.connect("posted_links.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS links (link TEXT PRIMARY KEY)")

# === Функції ===

def is_link_posted(link):
    cursor.execute("SELECT 1 FROM links WHERE link=?", (link,))
    return cursor.fetchone() is not None

def mark_link_as_posted(link):
    cursor.execute("INSERT INTO links VALUES (?)", (link,))
    conn.commit()

def contains_keywords(text):
    text = text.lower()
    return any(kw in text for kw in KEYWORDS + KEYWORDS_CRYPTO)

def get_image(entry):
    for link in entry.get("links", []):
        if link.get("type", "").startswith("image"):
            return link.get("href")
    return None

def format_text(title, summary):
    base = f"📰 <b>{title}</b>\n\n{summary}\n\n#новини #економіка"
    return base[:1024] + "..." if len(base) > 1024 else base

# === Головна логіка ===

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
                    print(f"⚠️ Помилка RSS: {feed_url} - {feed.bozo_exception}")
                    continue

                for entry in feed.entries:
                    link = entry.link
                    title = entry.title
                    summary = entry.get("summary", "")
                    image_url = get_image(entry)

                    if not image_url or is_link_posted(link):
                        continue
                    if not contains_keywords(title + summary):
                        continue
                    if is_blacklisted(title + summary):
                        continue

                    text = format_text(title, summary)

                    try:
                        await bot.send_photo(
                            chat_id=CHANNEL_ID,
                            photo=image_url,
                            caption=text
                        )
                        mark_link_as_posted(link)
                        print(f"✅ Опубліковано: {title}")
                    except Exception as e:
                        print(f"❌ Помилка надсилання: {e}")

                    await asyncio.sleep(10)

            except Exception as e:
                print(f"❌ Помилка джерела {feed_url}: {e}")

        await asyncio.sleep(1200)  # 20 хв

# === Запуск ===

if __name__ == "__main__":
    try:
        asyncio.run(fetch_and_post())
    except KeyboardInterrupt:
        print("⛔ Зупинено вручну")
    finally:
        conn.close()
