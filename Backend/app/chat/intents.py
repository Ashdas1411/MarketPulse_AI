from enum import Enum
from typing import Dict, List
from dataclasses import dataclass


class ChatIntent(str, Enum):
    MARKET_OVERVIEW = "market_overview"
    STOCK_SUMMARY = "stock_summary"
    NEWS_SUMMARY = "news_summary"
    EDUCATION = "education"
    GENERAL_HELP = "general_help"
    UNKNOWN = "unknown"


@dataclass
class IntentResult:
    intent: ChatIntent
    confidence: float
    entities: Dict[str, str]


# Keyword maps

INTENT_KEYWORDS = {
    ChatIntent.MARKET_OVERVIEW: [
        "market", "sensex", "nifty", "index", "indices"
    ],
    ChatIntent.STOCK_SUMMARY: [
        "stock", "share", "company", "price", "ticker"
    ],
    ChatIntent.NEWS_SUMMARY: [
        "news", "headline", "headlines", "latest"
    ],
    ChatIntent.EDUCATION: [
        "what is", "explain", "how does", "learn", "meaning"
    ],
    ChatIntent.GENERAL_HELP: [
        "help", "what can you do", "features", "capabilities"
    ],
}



# Intent detection

def detect_intent(message: str) -> IntentResult:
    if not message:
        return IntentResult(ChatIntent.UNKNOWN, 0.0, {})

    text = message.lower()
    scores: Dict[ChatIntent, int] = {}

    for intent, keywords in INTENT_KEYWORDS.items():
        scores[intent] = sum(1 for kw in keywords if kw in text)

    best_intent = max(scores, key=scores.get)
    best_score = scores[best_intent]

    if best_score == 0:
        return IntentResult(ChatIntent.UNKNOWN, 0.0, {})

    confidence = min(best_score / 3, 1.0)

    entities = {}
    for word in text.split():
        if word.isupper() or word.isalpha() and len(word) <= 5:
            entities["symbol"] = word.upper()

    return IntentResult(best_intent, confidence, entities)
