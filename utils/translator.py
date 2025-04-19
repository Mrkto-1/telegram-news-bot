# utils/translator.py

import requests

def translate_text(text, target_lang="uk"):
    try:
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "auto",
            "tl": target_lang,
            "dt": "t",
            "q": text,
        }
        response = requests.get(url, params=params)
        result = response.json()
        return "".join([item[0] for item in result[0]])
    except Exception as e:
        return f"[Переклад помилка] {e}"
