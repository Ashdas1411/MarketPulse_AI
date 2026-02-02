import requests
from fastapi import APIRouter
from app.config import GNEWS_API_KEY

def fetch_business_news():
    url = (
        "https://gnews.io/api/v4/top-headlines"
        "?category=business"
        "&lang=en"
        "&country=us"
        "&max=5"
        f"&apikey={GNEWS_API_KEY}"
    )
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        raise RuntimeError("Failed to fetch news from GNews")
    return response.json()

router = APIRouter()

@router.get("/api/v1/news")
def news():
    data = fetch_business_news()

    headlines = []
    for article in data.get("articles", []):
        headlines.append(article["title"])

    return {
        "status": "ok",
        "headlines": headlines
    }