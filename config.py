import os

# Токен бота з .env
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Telegram ID або @юзернейм каналу
CHANNEL_ID = -1002475588533  # Використовуємо ID, щоб точно працювало

# Активні години (від 6:00 до 2:00)
ACTIVE_HOURS = (6, 2)

# Теми, які пропускаємо
BLACKLIST = [
    "спорт", "мода", "музика", "кіно", "розваги", "серіали", "футбол",
    "гороскоп", "шоу", "культура"
]

# Ключові слова для фільтра
KEYWORDS = [
    "фрс", "ставка", "економіка", "інфляція", "криза", "рецесія", "s&p", "гроші"
]

# Криптовалюта — тільки критичні новини
KEYWORDS_CRYPTO = [
    "криптовалюта", "біткоїн", "bitcoin", "ethereum", "crypto"
]

# Дозволяємо лише українські джерела
RSS_FEEDS = [
    "https://www.epravda.com.ua/rss/",
    "https://www.ukrinform.ua/rss/economics",
    "https://biz.liga.net/ekonomika/rss.xml",
    "https://mind.ua/rss/news",
    "https://forbes.ua/rss"
]
