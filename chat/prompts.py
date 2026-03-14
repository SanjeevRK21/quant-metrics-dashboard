def base_prompt(
    ticker: str,
    start_date: str,
    end_date: str,
    event_name: str,
    event_outputs: dict,
    metric_guidance: str
) -> str:
    metrics_block = "\n".join(
        [f"- {k}: {v}" for k, v in event_outputs.items()]
    )

    return f"""
You are a professional financial analyst and educator.

Context:
Stock: {ticker}
Analysis Period: {start_date} to {end_date}
Analysis Type: {event_name}

Computed Metrics:
{metrics_block}

Your response MUST follow this structure:

PART 1 — Metric Interpretation
Explain what EACH metric represents and what the reported values indicate.

PART 2 — Investor Experience
Describe what holding this stock during this period would have felt like:
- volatility and emotional stress
- drawdowns or stability
- confidence or discomfort

PART 3 — Contextual & Scenario-Based Insight
Using general market knowledge (NOT price prediction):
- Explain plausible reasons why these metrics occurred
- Discuss what this risk/return profile TYPICALLY implies
- Emphasize uncertainty and scenario dependence

Important Rules:
- Do NOT give financial advice
- Do NOT predict future prices
- Do NOT claim certainty
- You MAY discuss risk regimes and typical behavior
- Keep explanations intuitive, grounded, and beginner-friendly

Metric-Specific Guidance:
{metric_guidance}
""".strip()


# Risk LLM prompt
def risk_metrics_prompt(ticker, start_date, end_date, event_outputs):
    return base_prompt(
        ticker,
        start_date,
        end_date,
        "Risk Metrics",
        event_outputs,
        """
Focus on:
- Volatility as day-to-day uncertainty
- Downside volatility as negative risk specifically
- Maximum drawdown as worst historical loss
Explain risk magnitude, not returns.
"""
    )


# Risk Adjusted LLM prompt
def risk_adjusted_metrics_prompt(ticker, start_date, end_date, event_outputs):
    return base_prompt(
        ticker,
        start_date,
        end_date,
        "Risk-Adjusted Metrics",
        event_outputs,
        """
Focus on:
- Sharpe ratio as return per unit of total risk
- Sortino ratio as return per unit of downside risk
- Calmar ratio as return relative to worst drawdown
Explain whether returns compensated for risk taken.
"""
    )


# Tail Risk LLM prompt
def tail_risk_metrics_prompt(ticker, start_date, end_date, event_outputs):
    return base_prompt(
        ticker,
        start_date,
        end_date,
        "Tail Risk Metrics",
        event_outputs,
        """
Focus on:
- Skewness as asymmetry of gains vs losses
- Kurtosis as frequency of extreme events
- VaR as a loss threshold under normal conditions
- CVaR as average loss during worst-case scenarios
Explain extreme risk, not average behavior.
"""
    )



# Market Sensitivity LLM prompt
def market_sensitivity_prompt(ticker, start_date, end_date, event_outputs):
    return base_prompt(
        ticker,
        start_date,
        end_date,
        "Market Sensitivity Metrics",
        event_outputs,
        """
Focus on:
- Beta as sensitivity to market movements
- Alpha as return unexplained by the market (daily if stated)
- R-squared as market dependency
Explain independence vs market-driven behavior.
"""
    )



# Stability LLM prompt
def stability_metrics_prompt(ticker, start_date, end_date, event_outputs):
    return base_prompt(
        ticker,
        start_date,
        end_date,
        "Stability Metrics",
        event_outputs,
        """
Focus on:
- Rolling Sharpe as consistency over time
- Underwater duration as time spent below prior peaks
- Recovery time as resilience after losses
Explain patience and reliability, not performance.
"""
    )


# Drawdown and Recovery LLM prompt
def drawdown_event_prompt(ticker, start_date, end_date, event_outputs):
    return base_prompt(
        ticker,
        start_date,
        end_date,
        "Drawdown Event",
        event_outputs,
        """
Focus on:
- Drawdown depth as severity of loss
- Decline duration as speed of fall
- Recovery time as healing period
- Total underwater time as emotional burden
Explain pain, recovery, and resilience.
"""
    )


# Investment Simulation LLM prompt
def investment_simulation_prompt(ticker, start_date, end_date, event_outputs):
    return base_prompt(
        ticker,
        start_date,
        end_date,
        "Investment Simulation",
        event_outputs,
        """
Focus on:
- Growth of invested capital
- Worst and best moments emotionally
- Large daily gains and losses as shocks
Explain the lived investment experience, not metrics.
"""
    )


