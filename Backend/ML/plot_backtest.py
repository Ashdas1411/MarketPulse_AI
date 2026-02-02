import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("ML/backtest_results.csv")
df["date"] = pd.to_datetime(df["date"])
df.set_index("date", inplace=True)
plt.figure(figsize=(12, 6))
plt.plot(df["capital"], label="Strategy Equity", linewidth=2)
plt.title("Equity Curve — ML Trading Strategy")
plt.xlabel("Date")
plt.ylabel("Capital Value")
plt.legend()
plt.grid(True)
plt.show()
rolling_max = df["capital"].cummax()
drawdown = (df["capital"] - rolling_max) / rolling_max
plt.figure(figsize=(12, 4))
plt.fill_between(drawdown.index, drawdown, color="red", alpha=0.3)
plt.title("Drawdown Curve")
plt.xlabel("Date")
plt.ylabel("Drawdown")
plt.grid(True)
plt.show()
