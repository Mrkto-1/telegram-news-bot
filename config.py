import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@worldnews_ua2025")

# Години активності (06:00 — 23:00)
ACTIVE_HOURS = (6, 23)

# Список ключових слів для фільтрації
KEYWORDS = [
    "фрс", "ставка", "економіка", "інфляція",
    "криза", "рецесія", "s&p", "s & p"
]

KEYWORDS_CRYPTO = [
    "криптовалюта", "біткоїн", "bitcoin", "ethereum", "crypto"
]

# Надійні українські джерела новин (економіка)
RSS_FEEDS = [
    "https://www.epravda.com.ua/rss/",                    # Економічна правда
    "https://biz.liga.net/ekonomika/rss.xml",           # Liga.net
    "https://mind.ua/rss/news",                         # Mind.ua
    "https://forbes.ua/rss"                              # Forbes Україна
]
