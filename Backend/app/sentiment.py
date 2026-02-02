from fastapi import APIRouter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from app.news import fetch_business_news

analyzer = SentimentIntensityAnalyzer()

def classify_sentiment(score):
    if score>=0.05:
        return "positive"
    elif score<=(-0.05):
        return "negative"
    else:
        return "neutral"
    
router = APIRouter()

@router.get("/api/v1/sentiment")
def sentiment():
    data = fetch_business_news()
    sentiment_results = []
    for article in data.get("articles", []):
        title = article["title"]
        score = analyzer.polarity_scores(title)["compound"]
        sentiment_results.append({
            "headline": title,
            "sentiment_score": round(score, 3)
        })
    return {
        "status": "ok",
        "sentiment": sentiment_results
    }