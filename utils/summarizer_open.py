from transformers import pipeline

# HuggingFace модель для зведення
summarizer = pipeline("summarization", model="google/pegasus-xsum")

def summarize_text(text):
    try:
        summary = summarizer(text, max_length=60, min_length=15, do_sample=False)
        return summary[0]["summary_text"]
    except Exception as e:
        return f"[⚠️ AI-зведення недоступне: {str(e)}]"
