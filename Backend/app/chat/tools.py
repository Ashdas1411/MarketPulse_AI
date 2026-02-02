from app.chat.intents import ChatIntent


def run_tool(intent: ChatIntent, entities: dict) -> dict:
    try:
        if intent == ChatIntent.MARKET_OVERVIEW:
            return {
                "tool": "market_overview",
                "status": "ok",
                "data": {
                    "direction": "up",
                    "change_percent": 0.11
                },
                "error": None
            }

        if intent == ChatIntent.NEWS_SUMMARY:
            return {
                "tool": "news_summary",
                "status": "ok",
                "data": [
                    "Global markets trade cautiously amid inflation concerns",
                    "Tech stocks show mixed performance in early trading",
                    "Oil prices stabilize after recent volatility"
                ],
                "error": None
            }

        if intent == ChatIntent.STOCK_SUMMARY:
            symbol = entities.get("symbol", "UNKNOWN")
            return {
                "tool": "stock_summary",
                "status": "ok",
                "data": {
                    "symbol": symbol,
                    "price": "195.30 USD",
                    "change_percent": "+0.8"
                },
                "error": None
            }

        return {
            "tool": "unknown",
            "status": "error",
            "data": None,
            "error": "No tool available"
        }

    except Exception as e:
        return {
            "tool": intent.value,
            "status": "error",
            "data": None,
            "error": str(e)
        }
