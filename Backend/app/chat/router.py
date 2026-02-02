from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import logging

from app.chat.intents import ChatIntent, detect_intent
from app.chat.tools import run_tool
from app.chat.formatter import format_response

router = APIRouter(prefix="/api/v1/chat", tags=["Chatbot"])
logger = logging.getLogger(__name__)


class ChatRequest(BaseModel):
    message: str
    symbol: Optional[str] = None
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    intent: str
    response: str
    data_sources: List[str]


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):

    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    if len(request.message) > 500:
        raise HTTPException(status_code=400, detail="Message too long.")

    finance_keywords = ["buy", "sell", "invest", "profit", "guarantee"]
    if any(word in request.message.lower() for word in finance_keywords):
        return ChatResponse(
            intent=ChatIntent.UNKNOWN.value,
            response="I do not provide financial or investment advice.",
            data_sources=[]
        )

    intent = detect_intent(request.message)
    logger.info(f"Detected intent: {intent.value}")

    tool_result = None
    if intent in {
        ChatIntent.MARKET_OVERVIEW,
        ChatIntent.NEWS_SUMMARY,
        ChatIntent.STOCK_SUMMARY,
    }:
        tool_result = run_tool(intent)

    response_text = format_response(intent, tool_result)

    data_sources = []
    if tool_result and tool_result.get("tool") != "unknown":
        data_sources.append(tool_result["tool"])

    return ChatResponse(
        intent=intent.value,
        response=response_text,
        data_sources=data_sources
    )
