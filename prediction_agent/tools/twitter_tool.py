import requests
import os
from dotenv import load_dotenv

load_dotenv()
BEARER_TOKEN = os.getenv("BEARER_TOKEN")


def search_tweets(query: str, max_results: int = 5) -> dict:
    if not BEARER_TOKEN:
        return {"status": "error", "error_message": "Missing Twitter BEARER_TOKEN."}

    url = "https://api.x.com/2/tweets/search/recent"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    params = {"query": query, "max_results": max_results}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        if "data" not in data or not data.get("data"):
            return {
                "status": "success",
                "report": f"No recent tweets found for '{query}'."
            }

        tweets = [tweet.get('text', '') for tweet in data['data']]
        report = "\n".join(f"- {tweet}" for tweet in tweets)
        return {
            "status": "success",
            "report": f"Top {len(tweets)} tweets for '{query}':\n{report}"
        }
    except requests.exceptions.RequestException as e:
        return {"status": "error", "error_message": str(e)}
