import asyncio
import feedparser
from aiogram import Bot, Dispatcher, types
from datetime import datetime
import os
from config import BOT_TOKEN, CHANNEL_ID, RSS_FEEDS
from utils.filters import is_relevant
from utils.translator import translate_text
from utils.summarizer_open import summarize_text  # open модель

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)
posted_links = set()
keywords_used_today = set()

KEYWORDS = ["фрс", "ставка", "інфляція", "економіка", "криза", "рецесія", "s&p", "s & p"]
KEYWORDS_CRYPTO = ["криптовалюта", "біткоїн", "bitcoin", "ethereum", "crypto"]
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


def get_emoji(keyword):
    mapping = {
        "фрс": "🏦", "ставка": "📈", "інфляція": "💸", "економіка": "📊", "криза": "⚠️",
        "рецесія": "📉", "s&p": "💹", "s & p": "💹",
        "криптовалюта": "🪙", "біткоїн": "₿", "bitcoin": "₿", "ethereum": "🧬", "crypto": "🪙"
    }
    return mapping.get(keyword, "🌍")


async def fetch_and_post():
    global FIRST_RUN
    while True:
        now = datetime.now()
        if not (6 <= now.hour < 24):
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
                summary = entry.get("summary", "")

                if link in posted_links:
                    continue

                if not contains_keywords(title):
                    continue

                main_kw = extract_main_keyword(title)
                if main_kw in keywords_used_today:
                    continue

                translated_title = translate_text(title)
                translated_summary = translate_text(summary)

                try:
                    ai_summary = summarize_text(summary)
                except Exception as e:
                    ai_summary = ""
                    print(f"❌ Summary error: {e}")

                emoji = get_emoji(main_kw)
                
                message = f"<b>{emoji} {translated_title}</b>\n"
                if ai_summary:
                    message += f"\n🧠 <i>{ai_summary}</i>"
                message += f"\n\n{translated_summary}"

                try:
                    await bot.send_message(CHANNEL_ID, message)
                    posted_links.add(link)
                    keywords_used_today.add(main_kw)
                    found += 1
                except Exception as e:
                    print(f"❌ Error posting: {e}")

        FIRST_RUN = False
        await asyncio.sleep(1200)  # 20 хв


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(fetch_and_post())
    loop.run_forever()
