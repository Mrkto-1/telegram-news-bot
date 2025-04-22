def is_relevant(title, summary, keywords):
    text = (title + " " + summary).lower()
    return any(kw in text for kw in keywords)
