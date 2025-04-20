import requests
import os

token = os.getenv("HF_API_TOKEN") or "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"
headers = {
    "Authorization": f"Bearer {token}"
}

API_URL = "https://api-inference.huggingface.co/models/DeepSeek-ai/deepseek-coder-6.7b-instruct"

def summarize_text(text, max_length=120, min_length=30):
    try:
        clean_text = text.replace("\n", " ").strip()
        trimmed = clean_text[:3000]  # max safe size for free HF inference

        prompt = f"Скороти цей текст до 2-3 речень українською мовою:\n\n{trimmed}"

        payload = {
            "inputs": prompt,
            "parameters": {
                "do_sample": False,
                "max_new_tokens": max_length
            }
        }

        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"].replace(prompt, "").strip()
        else:
            return "[Зведення недоступне]"
    except Exception as e:
        return f"[Помилка AI-зведення: {e}]"
