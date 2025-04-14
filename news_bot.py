import requests
import asyncio
from telegram import Bot

# Налаштування
TELEGRAM_TOKEN = '7870264120:AAEyLGcjffejYseO6ueDP0jcCKtyecVBhzc'
CHANNEL_ID = '@worldnews_ua2025'
NEWS_API_KEY = '7417d4f8ea7f49afaba2c36ed0371666'
NEWS_URL = 'https://newsapi.org/v2/top-headlines?language=en&category=general&pageSize=20'

bot = Bot(token=TELEGRAM_TOKEN)

async def get_world_news():
    response = requests.get(NEWS_URL, headers={'Authorization': NEWS_API_KEY})
    data = response.json()
    articles = data.get('articles', [])
    return articles if articles else []

async def translate_text(text):
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=uk&dt=t&q={requests.utils.quote(text)}"
    response = requests.get(url)
    if response.status_code == 200:
        translated_text = response.json()[0][0][0]
        return translated_text
    return text

async def send_news():
    while True:
        articles = await get_world_news()
        for article in articles:
            try:
                title = article.get('title', '')
                description = article.get('description', '')
                image_url = article.get('urlToImage')

                if title:
                    translated_title = await translate_text(title)
                    translated_description = await translate_text(description) if description else ""

                    message = f"🗞️ <b>Головна новина:</b>\n\n📰 <i>{translated_title}</i>\n\n📝 {translated_description}"

                    if image_url:
                        await bot.send_photo(chat_id=CHANNEL_ID, photo=image_url, caption=message, parse_mode="HTML")
                    else:
                        await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="HTML")

                    await asyncio.sleep(3)  # Пауза 3 секунди між новинами
            except Exception as e:
                print(f"Помилка при відправці новини: {e}")
        await asyncio.sleep(1200)  # Кожні 20 хвилин

if __name__ == "__main__":
    asyncio.run(send_news())
