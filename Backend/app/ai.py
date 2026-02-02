from huggingface_hub import InferenceClient
from app.config import HF_API_KEY

llama_client = InferenceClient(model="meta-llama/Meta-Llama-3-8B-Instruct",token = HF_API_KEY)

def llama_generate_explanation(prompt: str) -> str:
    response = llama_client.chat_completion(
        messages=[
            {
                "role": "system",
                "content": "You are a professional financial market analyst."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=180,
        temperature=0.4
    )
    return response.choices[0].message.content.strip()

def fallback_explanation(index, change_percent, direction, market_mood):
    return (
        f"Today, the {index} moved {direction} by {change_percent}%. "
        f"Overall market sentiment appears {market_mood}, based on recent financial news. "
        "Investors seem cautious, responding to a mix of economic signals and uncertainty. "
        "This summary is based on market data and sentiment analysis rather than predictive modeling."
    )

def generate_explanation(index, change_percent, direction, average_sentiment, sentiment_strength, market_mood):
    prompt = f"""
    You are a financial market analyst.
    Write a short, clear explanation (8-10 sentences) of today's market movement.
    Data:
    - Index: {index}
    - Market direction: {direction}
    - Percentage change: {change_percent}%
    - Average news sentiment score: {average_sentiment}
    - Sentiment strength: {sentiment_strength}
    Rules:
    - Do NOT give investment advice
    - Do NOT predict the future
    - Use simple, professional language
    """
    try:
        return llama_generate_explanation(prompt)
    except Exception as e:
        print("LLM generation failed:", e)
        return fallback_explanation(
            index=index,
            change_percent=change_percent,
            direction=direction,
            market_mood=market_mood
        )
    
def explain_trading_signal(signal, confidence, change_percent, avg_sentiment):
    """
    Generate an LLM-based explanation for the ML trading signal.
    """
    prompt = f"""
    You are a financial data analyst.
    Explain the following ML-generated market signal in neutral,
    informational terms only.

    Signal: {signal}
    Confidence scores: {confidence}
    Market change (%): {change_percent}
    Average news sentiment: {avg_sentiment}

    Rules:
    - Do NOT give advice or recommendations
    - Do NOT use words like "should", "buy", "sell", or "invest"
    - Do NOT suggest actions
    - Describe what the signal represents, not what to do
    - Use clear, factual, beginner-friendly language
    """
    try:
        return llama_generate_explanation(prompt)
    except Exception as e:
        print("LLM explanation failed:", e)
        return (
            f"The model generated a {signal} signal based on recent "
            f"market movement and news sentiment patterns."
        )