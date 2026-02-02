# 📊 MarketPulse_AI  
*A modular, backend-first market analytics and AI-ready intelligence platform*

MarketPulse_AI is a **production-oriented market intelligence backend** designed to explore how real-world financial systems, data pipelines, machine learning models, and conversational interfaces are built and connected in practice.

This project follows a **deterministic-first philosophy**: core logic, data pipelines, machine learning workflows, and safety guardrails are implemented **before** introducing large language models (LLMs). The focus is on correctness, explainability, and clean system design rather than shortcuts or hype.

---

## 🎯 Project Goals

- Build a **real, deployable backend system**, not a demo project  
- Learn **industry-grade backend and system architecture** step by step  
- Combine:
  - market data
  - financial news & sentiment analysis
  - machine learning signals
  - a controlled chatbot interface  
- Enforce **strict safety boundaries** (no financial advice)
- Create a project that is **interview-ready, explainable, and extensible**

---

<h2>🧱 Current Architecture</h2>

<pre>
MarketPulse_AI/
├── Backend/
│   ├── app/
│   │   ├── chat/
│   │   │   ├── intents.py        # Intent taxonomy & detection logic
│   │   │   ├── tools.py          # Deterministic backend tools (data-only)
│   │   │   ├── formatter.py     # Response formatting & safety guardrails
│   │   │   ├── router.py        # Chat API endpoint
│   │   │   └── prompts.py       # Reserved for future LLM integration
│   │   │
│   │   ├── market.py            # Market data logic
│   │   ├── news.py              # Financial news ingestion
│   │   ├── sentiment.py         # Sentiment analysis (VADER)
│   │   ├── trading.py           # ML signals & backtesting logic
│   │   ├── config.py
│   │   └── main.py              # FastAPI entry point
│   │
│   ├── ML/                      # ML experiments and trained models
│   └── requirements.txt
│
├── chatbot_scope.md             # Explicit chatbot safety scope
└── README.md
</pre>

---

## 🤖 Chatbot System (Core Focus)

The chatbot is **not** a free-form LLM wrapper.  
It is a **controlled, explainable decision system** built using clear layers.

### Chat Flow

User message
→ Intent detection (rule-based, scored)
→ Entity extraction (e.g., stock symbols)
→ Tool execution (pure data, no opinions)
→ Formatter (UX + safety + disclaimers)
→ API response


### Key Properties

- Finite, explicit intent taxonomy  
- One intent per request  
- Structured tool outputs (data only)  
- Context-aware guardrails  
- No predictions or financial advice  
- LLM-ready architecture (LLMs added later, not required)

This mirrors how regulated or production-grade conversational systems are designed.

---

## 📌 Implemented Features

### ✅ Market Overview
- Market direction and daily percentage change
- Deterministic API responses
- Formatter-controlled explanations

### ✅ Financial News & Sentiment
- Financial and business news ingestion
- Sentiment analysis using VADER
- Aggregated sentiment signals representing market mood

### ✅ Stock Summary (Informational)
- Symbol-based stock summaries
- Price and daily movement
- Clear non-advisory framing

### ✅ Machine Learning (Educational)
- Custom dataset generation
- BUY / SELL / HOLD classification model
- Walk-forward backtesting
- Equity curve and drawdown analysis
- Model persistence

> ML outputs are **educational signals only**, not recommendations.

### ✅ Chatbot Guardrails
- No financial or investment advice
- No future predictions
- No imperative language (e.g., “buy”, “sell”)
- Explicit uncertainty and informational framing

---

## 🧠 Design Philosophy

- Deterministic systems before generative AI  
- Data before language  
- Safety before scale  
- Explainability over hype  

Every layer is intentionally separated so it can be:
- tested
- audited
- reused
- extended

---

## 🚧 In Progress / Planned

- Frontend dashboard
- Database and persistence layer
- Authentication and user sessions
- Cloud deployment
- Advanced LLM-based response polishing
- UI/UX improvements
- Monetization strategies

---

## ⚠️ Disclaimer

This project is for **educational and informational purposes only**.  
It does **not** provide financial, investment, or trading advice.  
All market data and machine learning outputs are explanatory, not prescriptive.

---

## 👤 Author

**Arka Das**  
Student engineer building an end-to-end market analytics and AI-ready system  
with a focus on real-world architecture, safety, and clarity.

