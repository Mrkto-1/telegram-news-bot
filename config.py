# config.py
# Налаштування для новинного Telegram-бота "Світові новини щогодини! 🌍"

import os

# Токен Telegram-бота (має бути вказаний в .env або в налаштуваннях Railway)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ID або username Telegram-каналу для публікацій (для публічного каналу краще вказати @username)
# Якщо канал приватний, використовуй Chat ID формату -100xxxxxxxxxx
CHANNEL_ID = os.getenv("CHANNEL_ID", "-1002475588533")  # заміни при потребі

# Години активності бота (з 6:00 до 23:59)
ACTIVE_HOURS = (6, 24)

# Ключові слова, які вважаються релевантними для економічних новин
KEYWORDS = [
    "фрс", "ставка", "інфляція", "економіка", "криза", "рецесія", "s&p", "s & p",
    "нацбанк", "держборг", "інвестор", "облігації", "валюта", "ввп", "біржа"
]

# Криптовалютні ключові слова — тільки якщо новина критична
KEYWORDS_CRYPTO = [
    "криптовалюта", "біткоїн", "bitcoin", "ethereum", "crypto", "блокчейн", "SEC"
]

# Українські економічні RSS-джерела
RSS_FEEDS = [
    "https://www.epravda.com.ua/rss/",                  # Економічна правда 🇺🇦
    "https://www.ukrinform.ua/rss/economics",           # Укрінформ (економіка) 🇺🇦
    "https://biz.liga.net/ekonomika/rss.xml",           # Liga.net 🇺🇦
    "https://mind.ua/rss/news",                         # Mind.ua 🇺🇦
    "https://forbes.ua/rss"                             # Forbes Україна 🇺🇦
]
