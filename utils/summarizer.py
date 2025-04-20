from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text):
    try:
        text = text.strip()
        if not text or len(text.split()) < 20:
            return "[AI-зведення недоступне: надто короткий текст]"

        input_len = len(text.split())
        max_len = max(24, min(120, input_len // 2))
        min_len = max(10, min(40, input_len // 4))

        summary = summarizer(text, max_length=max_len, min_length=min_len, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return f"[AI-зведення недоступне] {e}"
