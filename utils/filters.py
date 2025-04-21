# utils/filters.py

# Теми, які не потрібно публікувати в Telegram-каналі
BLACKLIST = [
    "спорт", "мода", "музика", "кіно", "серіал", "розваги",
    "гороскоп", "ігри", "шоу", "футбол", "знаменитості"
]

def is_blacklisted(text: str) -> bool:
    """
    Повертає True, якщо в тексті знайдено хоча б одну заборонену тему.
    """
    text = text.lower()
    return any(word in text for word in BLACKLIST)
