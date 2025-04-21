import os

# 🔐 Токен Telegram-бота з оточення Railway
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 📢 Username відкритого каналу (Telegram дозволяє надсилати через username)
CHANNEL_ID = "@worldnews_ua2025"

# ⏰ Години активності (бот активний з 06:00 до 24:00)
ACTIVE_HOURS = (6, 24)

# 🧠 Основні ключові слова для економічних новин
KEYWORDS = [
    "фрс", "ставка", "економіка", "інфляція", "криза",
    "рецесія", "s&p", "s & p", "облікова", "бюджет"
]

# 🪙 Ключові слова для фільтрації новин про криптовалюту
KEYWORDS_CRYPTO = ["криптовалюта", "біткоїн", "bitcoin", "ethereum", "crypto"]

# 🌐 Стабільні українські економічні RSS-джерела
RSS_FEEDS = [
    "https://www.epravda.com.ua/rss/",                    # Економічна правда
    "https://www.ukrinform.ua/rss/economics",             # Укрінформ
    "https://biz.liga.net/ekonomika/rss.xml"              # Liga.net
]
