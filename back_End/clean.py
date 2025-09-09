import re

def clean_tweets(tweets):
    cleaned = []
    for text in tweets:
        text = re.sub(r'[^A-Za-z0-9\s]', '', text)   # symbols remove
        text = re.sub(r'\s+', ' ', text).strip()     # extra spaces remove
        cleaned.append(text)
    return cleaned
