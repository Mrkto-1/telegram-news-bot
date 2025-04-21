import os

# Основні налаштування
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Години активності бота (з 6:00 до 24:00)
ACTIVE_HOURS = (6, 24)

# Ключові слова для фільтрації новин
KEYWORDS = [
    "фрс", "ставка", "економіка", "інфляція",
    "криза", "рецесія", "s&p", "s & p"
]

# Ключові слова, пов'язані з криптовалютою
KEYWORDS_CRYPTO = [
    "криптовалюта", "біткоїн", "bitcoin", "ethereum", "crypto"
]

# Перевірені українські економічні RSS-джерела
RSS_FEEDS = [
    "https://www.epravda.com.ua/rss/",                          # Економічна правда
    "https://biz.liga.net/ekonomika/rss.xml",                   # Liga.net
    "https://www.unian.ua/static/rss/business.xml",             # УНІАН Бізнес
    "https://delo.ua/rss/all/",                                 # Delo.ua
    "https://www.unn.com.ua/rss/news/economics",               # Українські національні новини (економіка)
    "https://zn.ua/rss.xml"                                     # Дзеркало тижня
]
