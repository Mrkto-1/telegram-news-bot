import asyncio
import feedparser
from aiogram import Bot, Dispatcher, types
from datetime import datetime
import os
from config import BOT_TOKEN, CHANNEL_ID, RSS_FEEDS, ACTIVE_HOURS, BLACKLIST

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)
posted_links = set()
keywords_used_today = set()

KEYWORDS = ["фрс", "ставка", "інфляція", "економіка", "криза", "рецесія", "s&p", "s & p"]
KEYWORDS_CRYPTO = ["криптовалюта", "біткоїн", "bitcoin", "ethereum", "crypto"]


def contains_keywords(text):
    text_lower = text.lower()
    if any(kw in text_lower for kw in KEYWORDS):
        return True
    if any(kw in text_lower for kw in KEYWORDS_CRYPTO) and (
        "крах" in text_lower or "регулювання" in text_lower or "заборона" in text_lower
    ):
        return True
    return False


def extract_main_keyword(text):
    text_lower = text.lower()
    for kw in KEYWORDS + KEYWORDS_CRYPTO:
        if kw in text_lower:
            return kw
    return "економіка"


def is_ukrainian(text):
    return any("а" <= ch <= "я" or ch == "і" for ch in text.lower())


async def fetch_and_post():
    while True:
        now = datetime.now()
        hour = now.hour
        if not (ACTIVE_HOURS[0] <= hour or hour < ACTIVE_HOURS[1]):
            await asyncio.sleep(600)
            continue

        print("🔎 Перевірка новин...")

        for feed_url in RSS_FEEDS:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                title = entry.title
                link = entry.link
                summary = entry.get("summary", "")
                image_url = ""

                if link in posted_links:
                    continue

                if any(word.lower() in title.lower() for word in BLACKLIST):
                    continue

                if not contains_keywords(title):
                    continue

                if not is_ukrainian(title):
                    continue  # ❌ блокуємо неукраїнські новини

                main_kw = extract_main_keyword(title)
                if main_kw in keywords_used_today:
                    continue

                # спробуємо дістати зображення (media:content або links rel="enclosure")
                for l in entry.get("links", []):
                    if l.get("type", "").startswith("image"):
                        image_url = l.get("href", "")
                        break

                message = f"<b>🌍 {title}</b>\n\n{summary}\n\n#{main_kw.replace(' ', '')}\n\n🧠 Важливо   😴 Не цікаво"

                try:
                    if image_url:
                        await bot.send_photo(CHANNEL_ID, photo=image_url, caption=message)
                    else:
                        await bot.send_message(CHANNEL_ID, text=message)

                    print("✅ Опубліковано:", title)
                    posted_links.add(link)
                    keywords_used_today.add(main_kw)
                    await asyncio.sleep(10)
                except Exception as e:
                    print("❌ Помилка надсилання:", e)

        await asyncio.sleep(1200)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(fetch_and_post())
    loop.run_forever()
