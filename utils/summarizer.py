from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text):
    try:
        if not text or len(text.strip()) < 50:
            return "[AI-зведення недоступне]"
        summary = summarizer(text, max_length=120, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return f"[AI-зведення недоступне] {e}"
