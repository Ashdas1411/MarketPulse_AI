import yfinance as yf
from fastapi import APIRouter

from app.news import fetch_business_news
from app.sentiment import classify_sentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from app.ai import generate_explanation

analyzer = SentimentIntensityAnalyzer()

router = APIRouter()

@router.get("/api/v1/market")
def market():
    ticker = yf.Ticker("^GSPC")
    data = ticker.history(period="1d")
    if data.empty:
        return{"status":"Market_Closed","message":"Market is currently closed. No data available."}
    latest_open = data["Open"].iloc[0]
    latest_close = data["Close"].iloc[0]
    change_percent = ((latest_close-latest_open)/latest_open)*100
    direction = "up" if change_percent>=0 else "down"
    return {
        "index": "S&P 500",
        "open": round(latest_open, 2),
        "close": round(latest_close, 2),
        "change_percent": round(change_percent, 2),
        "direction":direction
    }

@router.get("/api/v1/market/pulse")
def market_pulse():
    # 1. Fetch market data
    ticker = yf.Ticker("^GSPC")
    data = ticker.history(period="1d")

    if data.empty:
        return {
            "status": "market_closed",
            "message": "Market is currently closed."
        }

    open_price = data["Open"].iloc[0]
    close_price = data["Close"].iloc[0]
    change_percent = ((close_price - open_price) / open_price) * 100
    direction = "up" if change_percent >= 0 else "down"

    # 2. Fetch news
    news_data = fetch_business_news()

    headlines_with_sentiment = []
    sentiment_scores = []

    # 3. Analyze sentiment
    for article in news_data.get("articles", []):
        title = article["title"]
        score = analyzer.polarity_scores(title)["compound"]

        headlines_with_sentiment.append({
            "headline": title,
            "sentiment_score": round(score, 3),
            "sentiment_label": classify_sentiment(score)
        })

        sentiment_scores.append(score)

    # 4. Aggregate sentiment
    average_sentiment = (
        sum(sentiment_scores) / len(sentiment_scores)
        if sentiment_scores else 0
    )

    if abs(average_sentiment) >= 0.25:
        sentiment_strength = "strong"
    elif abs(average_sentiment) >= 0.1:
        sentiment_strength = "moderate"
    else:
        sentiment_strength = "weak"

    if average_sentiment > 0.05:
        market_mood = "positive"
    elif average_sentiment < -0.05:
        market_mood = "negative"
    else:
        market_mood = "neutral"

    # 5. Generate explanation
    explanation = generate_explanation(
        index="S&P 500",
        change_percent=round(change_percent, 2),
        direction=direction,
        average_sentiment=round(average_sentiment, 3),
        sentiment_strength=sentiment_strength,
        market_mood=market_mood
    )


    # 6. Return response
    return {
        "status": "ok",
        "index": "S&P 500",
        "change_percent": round(change_percent, 2),
        "direction": direction,
        "market_mood": market_mood,
        "average_sentiment": round(average_sentiment, 3),
        "sentiment_strength": sentiment_strength,
        "headlines": headlines_with_sentiment,
        "explanation": explanation
    }
