# utils/filters.py

from config import BLACKLIST

def is_relevant(text):
    text = text.lower()
    return not any(bad in text for bad in BLACKLIST)
