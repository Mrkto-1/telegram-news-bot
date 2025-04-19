# utils/translator.py

import requests
from config import DEEPL_API_KEY

def translate_text(text, target_lang="UK"):
    try:
        response = requests.post(
            "https://api-free.deepl.com/v2/translate",
            data={
                "auth_key": DEEPL_API_KEY,
                "text": text,
                "target_lang": target_lang,
            },
        )
        return response.json()["translations"][0]["text"]
    except Exception as e:
        return f"[Переклад помилка] {e}"
