import joblib
import yfinance as yf
import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# ============================================================
# 1. Load trained ML artifacts
# ============================================================

model = joblib.load("ML/trading_model.pkl")
label_encoder = joblib.load("ML/label_encoder.pkl")

analyzer = SentimentIntensityAnalyzer()

# ============================================================
# 2. Backtest parameters
# ============================================================

START_CAPITAL = 100000
capital = START_CAPITAL
position = 0  # +1 = long, -1 = short, 0 = cash

results = []

print("Starting backtest...")

# ============================================================
# 3. Fetch historical market data
# ============================================================

ticker = yf.Ticker("^GSPC")
data = ticker.history(period="6mo", interval="1d")

if data.empty:
    raise RuntimeError("No historical data available")

# ============================================================
# 4. Walk-forward backtest (NO look-ahead bias)
# ============================================================

for i in range(1, len(data)):
    today = data.iloc[i]
    yesterday = data.iloc[i - 1]

    # --------------------------------------------------------
    # A. Features must come from YESTERDAY
    # --------------------------------------------------------

    yesterday_return = (
        yesterday["Close"] - yesterday["Open"]
    ) / yesterday["Open"]

    avg_sentiment = 0.0  # neutral sentiment for now

    X = np.array([[yesterday_return * 100, avg_sentiment]])

    # --------------------------------------------------------
    # B. Predict trading signal
    # --------------------------------------------------------

    prediction = model.predict(X)[0]
    signal = label_encoder.inverse_transform([prediction])[0]

    # --------------------------------------------------------
    # C. Position logic (decision for TODAY)
    # --------------------------------------------------------

    if signal == "BUY":
        position = 1
    elif signal == "SELL":
        position = -1
    else:
        position = 0

    # --------------------------------------------------------
    # D. Apply TODAY'S market return
    # --------------------------------------------------------

    today_return = (
        today["Close"] - today["Open"]
    ) / today["Open"]

    capital *= (1 + position * today_return)

    # --------------------------------------------------------
    # E. Store results
    # --------------------------------------------------------

    results.append({
        "date": today.name,
        "signal": signal,
        "daily_return": today_return,
        "position": position,
        "capital": capital
    })

# ============================================================
# 5. Save backtest results
# ============================================================

df = pd.DataFrame(results)
df.to_csv("ML/backtest_results.csv", index=False)

print("Backtest results saved to ML/backtest_results.csv")

# ============================================================
# 6. Performance metrics
# ============================================================

total_return = (capital - START_CAPITAL) / START_CAPITAL * 100
win_days = df[df["capital"].diff() > 0].shape[0]
total_days = df.shape[0]
win_rate = (win_days / total_days) * 100

print("\nBACKTEST RESULTS")
print("----------------")
print(f"Starting capital: {START_CAPITAL:.2f}")
print(f"Final capital:    {capital:.2f}")
print(f"Total return:     {total_return:.2f}%")
print(f"Win rate:         {win_rate:.2f}%")
