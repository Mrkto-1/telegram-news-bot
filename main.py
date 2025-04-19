import asyncio
import feedparser
from aiogram import Bot, Dispatcher, types
from datetime import datetime
import random

from config import BOT_TOKEN, CHANNEL_ID, ACTIVE_HOURS, RSS_FEEDS
from utils.filters import is_relevant
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

        found = False  # щоби публікувати лише 1 новину за раз

        for feed_url in RSS_FEEDS:
            if found:
                break

            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                title = entry.title
                link = entry.link

                if link in posted_links or not is_relevant(title):
                    continue

                translated_title = translate_text(title)
                message = f"📉 <b>{translated_title}</b>\n\n🔗 <a href='{link}'>Читати повністю</a>"

                try:
                    await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode=types.ParseMode.HTML)
                    posted_links.add(link)
                    found = True
                    break  # опублікували 1 новину → виходимо з циклу
                except Exception as e:
                    print(f"❌ Помилка надсилання: {e}")

        await asyncio.sleep(random.randint(1200, 1800))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_and_post())
