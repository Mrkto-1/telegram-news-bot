import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@worldnews_ua2025"

ACTIVE_HOURS = (6, 24)
BLACKLIST = ["спорт", "мода", "музика", "кіно", "розваги", "серіали", "футбол"]

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

RSS_FEEDS = [
    "https://feeds.reuters.com/reuters/businessNews",
    "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "https://www.marketwatch.com/rss/topstories",
]
