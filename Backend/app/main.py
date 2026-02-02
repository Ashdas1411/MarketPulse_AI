from fastapi import FastAPI

from app.news import router as news_router
from app.sentiment import router as sentiment_router
from app.market import router as market_router
from app.trading import router as trading_router
from app.chat.router import router as chat_router

app = FastAPI()

app.include_router(news_router)
app.include_router(sentiment_router)
app.include_router(market_router)
app.include_router(trading_router)
app.include_router(chat_router)

@app.get("/")
def root():
    return {"message": "MarketPulse AI backend running!!!"}