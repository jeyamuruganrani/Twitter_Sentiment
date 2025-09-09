import matplotlib.pyplot as plt
import pandas as pd


def table_view(data):
    df = pd.DataFrame(data)

    # Sentiment counts
    sentiment_counts = df["sentiment"].value_counts()

    # Plot
    plt.figure(figsize=(6, 4))
    plt.bar(sentiment_counts.index, sentiment_counts.values)
    plt.xlabel("Sentiment")
    plt.ylabel("Count")
    plt.title("Sentiment Distribution of Tweets")
    plt.show()