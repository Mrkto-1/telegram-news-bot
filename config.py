import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "CHANNEL_ID = "-1002475588533"
"

ACTIVE_HOURS = (6, 24)

BLACKLIST = ["спорт", "мода", "музика", "кіно", "розваги", "серіали", "футбол"]

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # не використовується поки
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")    # теж ні

# ДОДАНІ RSS з українських економічних джерел
RSS_FEEDS = [
    "https://feeds.reuters.com/reuters/businessNews",                # англомовне
    "https://www.cnbc.com/id/100003114/device/rss/rss.html",         # англомовне
    "https://www.marketwatch.com/rss/topstories",                    # англомовне
    
    "https://www.epravda.com.ua/rss/",                                # 🇺🇦 Економічна правда
    "https://www.ukrinform.ua/rss/economics",                         # 🇺🇦 Укрінформ
    "https://biz.liga.net/ekonomika/rss.xml",                         # 🇺🇦 Liga.net
    "https://mind.ua/rss/news",                                       # 🇺🇦 Mind.ua
    "https://forbes.ua/rss"                                           # 🇺🇦 Forbes Україна
]
