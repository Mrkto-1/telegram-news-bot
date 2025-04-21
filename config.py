import os

# Токени
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Години активності бота (6:00–23:00)
ACTIVE_HOURS = (6, 23)

# Ключові слова — новини, що нас цікавлять
KEYWORDS = [
    "фрс", "ставка", "інфляція", "економіка", "криза",
    "рецесія", "s&p", "s & p"
]

# Новини про крипту — тільки якщо щось важливе
KEYWORDS_CRYPTO = [
    "криптовалюта", "біткоїн", "bitcoin", "ethereum", "crypto"
]

# 🔥 Тільки валідні українські джерела
RSS_FEEDS = [
    "https://www.epravda.com.ua/rss/",
    "https://biz.liga.net/ekonomika/rss.xml",
    "https://delo.ua/rss/all/",
    "https://zn.ua/rss.xml",
    "https://www.unian.ua/static/rss/business.xml",
    "https://interfax.com.ua/news/economic.rss"
]
