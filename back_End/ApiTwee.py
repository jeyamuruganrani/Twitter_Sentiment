import time
import tweepy
import Bert

# ================== AUTH ==================
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAADQY4AEAAAAAvspBxUH%2BVjX2ppGXCVsVlJsvVHQ%3DL4vOu9qckcQjH5GPMs7tR3x0sD73rpn912MYTtqGl3OMoqqP6J"  # 🔒 put in .env in production

client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    wait_on_rate_limit=True  # Tweepy auto-sleeps on rate limit
)


# ================== FETCH ==================
def fetch_tweets(query: str, max_results: int = 100, pages: int = 1, retries: int = 3):
    """
    Fetch recent tweets for a given query with pagination + retries.

    Args:
        query (str): Search keyword
        max_results (int): Number of tweets per request (max 100)
        pages (int): Number of pages to fetch
        retries (int): Retry attempts on rate-limit or errors

    Returns:
        list: List of tweets (dict with id, text, author_id, created_at, lang)
    """
    all_tweets = []
    next_token = None

    for page in range(pages):
        attempt = 0
        while attempt < retries:
            try:
                response = client.search_recent_tweets(
                    query=query,
                    max_results=max_results,
                    tweet_fields=["created_at", "author_id", "lang"],
                    next_token=next_token
                )

                if not response.data:
                    print("⚠️ No tweets found on this page.")
                    return all_tweets

                # Collect tweets
                for tweet in response.data:
                    all_tweets.append({
                        "id": tweet.id,
                        "text": tweet.text,
                        "author_id": tweet.author_id,
                        "created_at": tweet.created_at,
                        "lang": tweet.lang
                    })

                print(f"✅ Page {page+1} fetched {len(response.data)} tweets.")

                # Pagination
                next_token = response.meta.get("next_token")
                if not next_token:
                    print("📌 No more pages available.")
                    return all_tweets

                # small delay to avoid hitting limit too fast
                time.sleep(2)
                break  # exit retry loop

            except tweepy.TooManyRequests as e:
                reset_time = int(e.response.headers.get("x-rate-limit-reset", time.time() + 60))
                sleep_for = max(reset_time - int(time.time()), 60)
                print(f"⏳ Rate limit exceeded. Sleeping for {sleep_for} seconds...")
                time.sleep(sleep_for)
                attempt += 1

            except Exception as e:
                print(f"❌ Error: {e}")
                attempt += 1
                time.sleep(5)

    return all_tweets


# ================== RUN ==================
if __name__ == "__main__":
    query = "Mahindra Thar Roxx"
    max_results = 10     # tweets per page (max 100)
    pages = 3           # how many pages to fetch

    tweets = fetch_tweets(query, max_results=max_results, pages=pages)

    print(f"\n📊 Total Tweets Fetched: {len(tweets)}\n")
    if tweets:
        # Extract text only
        tweet_texts = [t["text"] for t in tweets]

        # Run Sentiment Analysis
        sentiments = Bert.BERT_text(tweet_texts)

        # Print results with metadata
        print(sentiments)