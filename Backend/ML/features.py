import pandas as pd

def build_features(change_percent: float, avg_sentiment: float) -> pd.DataFrame:
    """
    Create a feature DataFrame for ML models.
    This function MUST be used everywhere:
    - training
    - inference
    - backtesting
    """

    features = {
        "change_percent": change_percent,
        "avg_sentiment": avg_sentiment
    }

    return pd.DataFrame([features])
