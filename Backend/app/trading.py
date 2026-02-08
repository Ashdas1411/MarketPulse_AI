import joblib
import numpy as np
import yfinance as yf

from fastapi import APIRouter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from app.news import fetch_business_news
from app.ai import explain_trading_signal

# Creating router
router = APIRouter()

# Loading trained ML artifacts ONCE (at startup)
model = joblib.load("ML/trading_model.pkl")
label_encoder = joblib.load("ML/label_encoder.pkl")

# Sentiment analyzer
analyzer = SentimentIntensityAnalyzer()


@router.get("/api/v1/trading/signal")
def trading_signal():
    """
    ML-powered trading signal endpoint.
    Returns BUY / SELL / HOLD with confidence scores
    and an LLM-generated explanation.
    """

    # 1. Fetching market data
    ticker = yf.Ticker("^GSPC")
    data = ticker.history(period="1d")

    if data.empty:
        return {
            "status": "market_closed",
            "message": "Market data unavailable."
        }

    open_price = data["Open"].iloc[0]
    close_price = data["Close"].iloc[0]

    change_percent = ((close_price - open_price) / open_price) * 100

    # 2. Fetching news and compute average sentiment
    news_data = fetch_business_news()
    sentiment_scores = []

    for article in news_data.get("articles", []):
        score = analyzer.polarity_scores(article["title"])["compound"]
        sentiment_scores.append(score)

    avg_sentiment = (
        sum(sentiment_scores) / len(sentiment_scores)
        if sentiment_scores else 0
    )

    # 3. Preparing ML input (same feature order as training)
    X = np.array([[change_percent, avg_sentiment]])

    # 4. Predicting class
    prediction = model.predict(X)[0]
    signal = label_encoder.inverse_transform([prediction])[0]

    # 5. Predicting confidence scores
    probabilities = model.predict_proba(X)[0]
    class_labels = label_encoder.classes_

    confidence_scores = {
        class_labels[i]: round(float(probabilities[i]), 3)
        for i in range(len(class_labels))
    }

    # 6. Generating LLM explanation
    explanation = explain_trading_signal(
        signal=signal,
        confidence=confidence_scores,
        change_percent=round(change_percent, 2),
        avg_sentiment=round(avg_sentiment, 3)
    )

    # 7. Returning response
    return {
        "status": "ok",
        "signal": signal,
        "confidence": confidence_scores,
        "change_percent": round(change_percent, 2),
        "average_sentiment": round(avg_sentiment, 3),
        "explanation": explanation
    }
