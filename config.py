import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "-1002475588533"
ACTIVE_HOURS = (6, 24)

BLACKLIST = ["спорт", "мода", "музика", "кіно", "розваги", "серіали", "футбол"]

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

RSS_FEEDS = [
    "https://feeds.reuters.com/reuters/businessNews",
    "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "https://www.marketwatch.com/rss/topstories",
    "https://www.epravda.com.ua/rss/",
    "https://www.ukrinform.ua/rss/economics",
    "https://biz.liga.net/ekonomika/rss.xml",
    "https://mind.ua/rss/news",
    "https://forbes.ua/rss"
]
