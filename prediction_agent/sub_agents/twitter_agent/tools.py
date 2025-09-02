import requests
import os
from dotenv import load_dotenv

load_dotenv()
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
MOCK_TWITTER = os.getenv("MOCK_TWITTER", "FALSE").upper() == "TRUE"
#dummyResponse = "It's dummy Response"
dummyResponse = """
Bangkok has emerged as a top travel destination, particularly for Gen Z, due to its vibrant culture and affordability, while Thailand’s tourism initiatives like free domestic flights and cryptocurrency payment systems are enhancing its appeal. Infrastructure upgrades, including Suvarnabhumi Airport’s expansion and Banthat Thong Road’s transformation into a street food hub, are generating buzz for improving the visitor experience. However, mixed sentiments on X highlight both praise for Bangkok’s food and nightlife and concerns about safety, pollution, and chaotic conditions.Top Gen Z Destination: Bangkok tops global rankings for Gen Z travelers, driven by its nightlife, culture, and new attractions like the world’s largest POP MART store.
Tourism Initiatives: Thailand’s 700 million baht flight subsidies and TouristDigiPay crypto system, alongside airport and street food upgrades, aim to boost Bangkok’s tourism.
Mixed Experiences: X posts reflect polarized views, with some praising Bangkok’s culinary scene and others criticizing its safety and cleanliness issues.
"""
def search_tweets(query: str, max_results: int = 5) -> dict:
    if MOCK_TWITTER:
        print("Mocking TWITTER data")
        return {
            "status": "success",
            "latestTweets": f"Query is: {query}\n. Respose: {dummyResponse}"
        }
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