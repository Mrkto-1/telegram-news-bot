import os

# 🔐 Токен твого Telegram-бота
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 📢 ID каналу, куди бот буде надсилати новини (без @)
CHANNEL_ID = "-1002475588533"

# ⏰ Час, коли бот активний (з 6:00 до 24:00 ночі)
ACTIVE_HOURS = (6, 24)

# ❌ Теми, які потрібно ігнорувати
BLACKLIST = [
    "спорт", "мода", "музика", "кіно", "розваги", "серіали", "футбол"
]

# 📡 RSS-джерела (лише українські або ті, де часто є український контент)
RSS_FEEDS = [
    "https://www.epravda.com.ua/rss/",
    "https://www.ukrinform.ua/rss/economics",
    "https://biz.liga.net/ekonomika/rss.xml",
    "https://mind.ua/rss/news",
    "https://forbes.ua/rss"
]
