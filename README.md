# Quantitative Stock Analysis & Research Platform
A full-stack institutional-grade quantitative analysis platform that evaluates stocks using multi-layer risk analytics, investment simulation, and AI-powered research interpretation.
This system combines:
- Advanced financial metrics (8+ analytical pipelines)
- Interactive visual dashboard (Flask + Tailwind UI)
- AI research assistant (LLM-powered insights via Ollama)
- Investment simulation engine

## Overview
This platform transforms raw market data into actionable financial insights through:
```
Market Data → Quant Metrics → Risk Analysis → Simulation → AI Interpretation → Interactive Dashboard
```
Users can:
- Analyze any stock across custom date ranges
- Evaluate risk, returns, and tail behavior
- Simulate investment outcomes
- Explore drawdowns and recovery patterns
- Ask questions via an AI research chatbot

## Core Features
### Data Engine
- Fetches historical stock data using Yahoo Finance
- Supports full-range and custom time windows  
👉 Implemented in: [`data_loader.py`](./data_loader.py)

### Returns Engine
- Computes log returns for accurate statistical modeling  
👉 Implemented in: [`returns.py`](./returns.py)

### Growth Metrics
- Total Return
- CAGR (Compound Annual Growth Rate)  
👉 Implemented in: [`growth.py`](./growth.py)

### Risk Metrics
- Annualized Volatility
- Downside Volatility
- Maximum Drawdown  
👉 Implemented in: [`risk.py`](./risk.py)

### Risk-Adjusted Metrics
- Sharpe Ratio
- Sortino Ratio
- Calmar Ratio  
👉 Implemented in: [`risk_adjusted.py`](./risk_adjusted.py)

### Tail Risk Analysis
- Skewness (asymmetry)
- Excess Kurtosis (fat tails)
- Value at Risk (VaR)
- Conditional VaR (CVaR)  
👉 Implemented in: [`tail_risk.py`](./tail_risk.py)

### Market Sensitivity
- Beta (market exposure)
- Alpha (excess return)
- R² (market dependency)  
👉 Implemented in: [`market.py`](./market.py)

### Stability Metrics
- Rolling Sharpe Ratio
- Drawdown Duration
- Recovery Time  
👉 Implemented in: [`stability.py`](./stability.py)

### Drawdown Event Analysis
```
Extracts full drawdown → trough → recovery cycles
```
Measures duration, severity, and recovery time  
👉 Implemented in: [`drawdown_events.py`](./drawdown_events.py)

### Investment Simulator
Simulates capital growth over time
Tracks:
- Final portfolio value
- Max gain / loss days
- Min / max portfolio levels  
👉 Implemented in: [`investment_simulator.py`](./investment_simulator.py)

## AI Research Layer
### Quant Research Chatbot
- LLM-powered assistant (via Ollama / Phi-3)
- Answers questions using computed metrics
Provides:
- Interpretations
- Contextual reasoning
- Investor insights  
👉 Implemented in: [`research_chatbot.py`](./research_chatbot.py)

### Context Builder
Structures all computed metrics into LLM-ready format  
👉 Implemented in: [`context_builder.py`](./context_builder.py)

### Prompt Engineering Layer
Specialized prompts for:
- Growth
- Risk
- Adjusted Risk
- Tail risk
- Market sensitivity
- Stability
- Investment simulation  
👉 Implemented in: [`prompts.py`](./prompts.py)

### Event-Level Explanation Engine
- Routes different analyses to appropriate prompt templates
- Generates structured financial explanations  
👉 Implemented in: [`events_explainer.py`](./events_explainer.py)

## Web Application
### Flask Backend
Handles:
- Data processing
- Metric computation
- Chart generation (base64 encoded images)
- API endpoints  
👉 Implemented in: [`app.py`](./app.py)

### Interactive Dashboard UI
- Base Layout
- Animated aurora background
- Neon grid + particle effects
- Sidebar navigation  
👉 Implemented in: [`base.html`](./base.html)

### Analysis Dashboard
- Input controls (ticker, date range, capital)
- Metric cards
- Charts & visual analytics
- Drawdown tables
- Integrated AI chatbot  
👉 Implemented in: [`index.html`](./index.html)

### Visual Analytics
The platform generates:
- Price Series
- Cumulative Returns (Growth of $1)
- Rolling Volatility
- Drawdown Charts
- Return Distribution (VaR & CVaR)
- Daily P&L
- Rolling Sharpe
- Market Beta Scatter Plot
(All dynamically generated via matplotlib and encoded for web display)

## System Architecture
```
Frontend (Tailwind UI)
        ↓
Flask API Layer
        ↓
Quant Engine (Metrics Pipelines)
        ↓
Simulation + Event Analysis
        ↓
Context Builder
        ↓
LLM (Ollama / API)
        ↓
Insights + Visualization
```

## Project Structure
```
.
├── app.py
├── templates/
│   ├── base.html
│   ├── index.html
│
├── engine/
│   ├── data_loader.py
│   ├── returns.py
│   ├── growth.py
│   ├── risk.py
│   ├── risk_adjusted.py
│   ├── tail_risk.py
│   ├── stability.py
│   ├── market.py
│   ├── drawdown_events.py
│   ├── investment_simulator.py
│
├── chat/
│   ├── research_chatbot.py
│   ├── prompts.py
│   ├── event_explainer.py
│   ├── context_builder.py
│
└── README.md
```

## Installation
```
git clone https://github.com/your-username/quant-analysis-platform.git
cd quant-analysis-platform

pip install -r requirements.txt
```

## Required Libraries
- flask
- pandas
- numpy
- matplotlib
- yfinance
- scipy

## Running the App
```
python app.py
```
Open:
```
http://127.0.0.1:5000/

```

## Enabling AI Chatbot
To use the research chatbot:
1. Install Ollama
2. Run a model (e.g. Phi-3)
```
ollama run phi3
```
3. Ensure API is available at:
```
http://localhost:11434
```

## Key Highlights
- Multi-layer quant engine (8+ pipelines)
- Institutional-grade risk analytics
- LLM-powered financial interpretation
- Drawdown & recovery intelligence
- Investment simulation engine
- Highly interactive futuristic UI

## Future Improvements
- Portfolio optimization (mean-variance, risk parity)
- Factor models (Fama-French)
- Backtesting engine
- Cloud deployment (Docker + AWS)
- Real-time streaming data
- Multi-asset support

## Disclaimer
This project is for educational and research purposes only and does not constitute financial advice.

## Author
Sanjeev Raj
