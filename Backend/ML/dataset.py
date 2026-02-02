import yfinance as yf
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def classify_label(change_percent, sentiment_score):
    """
    Weak-supervision labeling that guarantees class diversity
    while staying financially reasonable.
    """

    # Strong upward move → BUY
    if change_percent > 0.15:
        return "BUY"

    # Strong downward move → SELL
    elif change_percent < -0.15:
        return "SELL"

    # Everything else → HOLD
    else:
        return "HOLD"
    
def generate_dataset(
    symbol="^GSPC",
    period="1y",
    output_file="ml/training_data.csv"
):
    """
    Generates a labeled dataset using historical price data
    and simulated sentiment scores.
    """

    # 1. Fetch historical market data
    ticker = yf.Ticker(symbol)
    data = ticker.history(period=period)

    if data.empty:
        raise RuntimeError("Failed to fetch market data")

    rows = []

    # 2. Iterate over each trading day
    for i in range(len(data)):
        open_price = data["Open"].iloc[i]
        close_price = data["Close"].iloc[i]

        # Skip invalid data
        if open_price == 0:
            continue

        change_percent = ((close_price - open_price) / open_price) * 100

        # 3. Simulate sentiment (for now)
        # NOTE: Real sentiment will come later
        sentiment_score = analyzer.polarity_scores(
            f"Market moved {change_percent:.2f} percent today"
        )["compound"]

        # 4. Assign label using rule-based logic
        label = classify_label(change_percent, sentiment_score)

        rows.append([
            round(change_percent, 3),
            round(sentiment_score, 3),
            label
        ])

    # 5. Create DataFrame
    df = pd.DataFrame(
        rows,
        columns=["change_percent", "average_sentiment", "label"]
    )

    # 6. Save dataset
    df.to_csv(output_file, index=False)

    print(f"Dataset created with {len(df)} rows")
    print(f"Saved to {output_file}")


if __name__ == "__main__":
    generate_dataset()
