from app.chat.intents import ChatIntent, IntentResult


ADVICE_KEYWORDS = {"buy", "sell", "invest", "profit", "guarantee"}


def format_response(
    intent_result: IntentResult,
    tool_result: dict | None,
    original_message: str
) -> str:

    text = original_message.lower()

    if any(word in text for word in ADVICE_KEYWORDS):
        return (
            "I can share market information and explain concepts, "
            "but I don’t provide investment or financial advice."
        )

    intent = intent_result.intent

    if intent == ChatIntent.MARKET_OVERVIEW:
        data = tool_result.get("data") if tool_result else None
        if not data:
            return "Market data is currently unavailable."

        return (
            "Here’s a snapshot of the overall market.\n\n"
            f"The market is moving {data['direction']} "
            f"with a change of about {data['change_percent']}%.\n\n"
            "This reflects recent index movement, not future performance."
        )

    if intent == ChatIntent.NEWS_SUMMARY:
        headlines = tool_result.get("data") if tool_result else None
        if not headlines:
            return "Financial news is currently unavailable."

        return "Recent financial headlines:\n\n" + "\n".join(
            f"{i+1}. {h}" for i, h in enumerate(headlines)
        )

    if intent == ChatIntent.STOCK_SUMMARY:
        data = tool_result.get("data") if tool_result else None
        if not data:
            return "Stock data is currently unavailable."

        return (
            f"Here is a general overview of {data['symbol']}.\n\n"
            f"Current price: {data['price']}\n"
            f"Day change: {data['change_percent']}%\n\n"
            "This is informational only and not a recommendation."
        )

    if intent == ChatIntent.EDUCATION:
        return (
            "The stock market allows investors to buy ownership shares "
            "in publicly listed companies.\n\n"
            "Prices change based on supply, demand, and expectations."
        )

    if intent == ChatIntent.GENERAL_HELP:
        return (
            "I can explain market concepts, summarize news, "
            "and provide general market and stock information."
        )

    return "I’m not sure how to help with that yet."
