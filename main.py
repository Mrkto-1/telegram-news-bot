import asyncio
import feedparser
from aiogram import Bot, Dispatcher, types
from datetime import datetime
import random

from config import BOT_TOKEN, CHANNEL_ID, ACTIVE_HOURS, RSS_FEEDS
from utils.filters import is_relevant
from utils.summarizer import summarize_text
from utils.translator import translate_text

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
posted_links = set()

async def fetch_and_post():
    while True:
        now_hour = datetime.now().hour
        if not (ACTIVE_HOURS[0] <= now_hour < ACTIVE_HOURS[1]):
            await asyncio.sleep(600)
            continue

        for feed_url in RSS_FEEDS:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:5]:
                title = entry.title
                link = entry.link

                if link in posted_links or not is_relevant(title):
                    continue

                summary = summarize_text(entry.summary if 'summary' in entry else title)
                translation = translate_text(summary)

                message = f"📉 <b>{title}</b>\n\n🧠 {translation}\n🌍 <a href='{link}'>Джерело</a>"

                try:
                    await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode=types.ParseMode.HTML)
                    posted_links.add(link)
                    await asyncio.sleep(5)
                except Exception as e:
                    print(f"❌ Помилка надсилання: {e}")

        await asyncio.sleep(random.randint(1200, 1800))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_and_post())
