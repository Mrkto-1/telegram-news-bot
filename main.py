import os
import asyncio
import feedparser
from aiogram import Bot, Dispatcher
from aiogram.types import InputMediaPhoto
from datetime import datetime
from utils.filters import is_relevant
from utils.translator import translate_text

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

RSS_FEEDS = [
    "https://www.epravda.com.ua/rss/",
    "https://www.ukrinform.ua/rss/economics",
    "https://biz.liga.net/ekonomika/rss.xml",
    "https://mind.ua/rss/news",
    "https://forbes.ua/rss"
]

ACTIVE_HOURS = (6, 2)
POSTED_LINKS = set()
KEYWORDS = ["фрс", "ставка", "інфляція", "економіка", "криза", "рецесія", "s&p", "s & p"]
KEYWORDS_CRYPTO = ["криптовалюта", "біткоїн", "bitcoin", "ethereum", "crypto"]

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)


def contains_keywords(text):
    text = text.lower()
    return any(kw in text for kw in KEYWORDS + KEYWORDS_CRYPTO)


def get_image(entry):
    for link in entry.get("links", []):
        if link.get("type", "").startswith("image"):
            return link.get("href")
    return None


async def fetch_and_post():
    while True:
        now = datetime.now()
        if not (ACTIVE_HOURS[0] <= now.hour < ACTIVE_HOURS[1]):
            await asyncio.sleep(600)
            continue

        for feed_url in RSS_FEEDS:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                link = entry.link
                title = entry.title
                summary = entry.get("summary", "")
                image_url = get_image(entry)

                if not image_url:
                    continue

                if link in POSTED_LINKS:
                    continue

                if not contains_keywords(title):
                    continue

                text = f"<b>🌍 {title}</b>\n\n{summary}"

                try:
                    await bot.send_photo(CHANNEL_ID, photo=image_url, caption=text[:1024], parse_mode="HTML")
                    POSTED_LINKS.add(link)
                except Exception as e:
                    print(f"Send error: {e}")

                await asyncio.sleep(5)

        await asyncio.sleep(1200)  # 20 хв


if __name__ == "__main__":
    asyncio.run(fetch_and_post())
