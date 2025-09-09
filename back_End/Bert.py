from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import matplotlib.pyplot as plt
import numpy as np
import json
# Load Model
model_name = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Label mapping
labels_map = {0: "Negative", 1: "Neutral", 2: "Positive"}

def BERT_text(tweets):
    results = []
    # Predict
    for tweet in tweets:
        result = sentiment_pipeline(tweet)[0]
        label_id = int(result['label'].split("_")[-1])  # extract number from LABEL_X
        sentiment = labels_map[label_id]
        results.append({
            "tweet": tweet,
            "sentiment": sentiment,
            "score": result['score']
        })

    with open("re.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print("📁 Results saved to re.json")

    return  results


