import re

def clean_tweets(tweets):
    cleaned = []
    for text in tweets:
        # remove hashtags
        text = re.sub(r'#\S+', '', text)
        # remove mentions (@username)
        text = re.sub(r'@\S+', '', text)
        # remove links (http or https)
        text = re.sub(r'http\S+', '', text)
        # remove extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        cleaned.append(text)
    return cleaned
