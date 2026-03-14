# chat/context_builder.py

def build_research_context(
    ticker: str,
    start_date: str,
    end_date: str,
    growth_outputs: dict,
    risk_outputs: dict,
    risk_adjusted_outputs: dict,
    tail_risk_outputs: dict,
    market_outputs: dict,
    stability_outputs: dict,
    investment_outputs: dict
) -> str:

    def format_block(title, block):
        formatted = f"\n--- {title} ---\n"
        for k, v in block.items():
            formatted += f"{k}: {v}\n"
        return formatted

    context = f"""
==============================
STOCK ANALYSIS DATA
==============================

Ticker: {ticker}
Period: {start_date} to {end_date}
"""

    context += format_block("Growth Metrics", growth_outputs)
    context += format_block("Risk Metrics", risk_outputs)
    context += format_block("Risk-Adjusted Metrics", risk_adjusted_outputs)
    context += format_block("Tail Risk Metrics", tail_risk_outputs)
    context += format_block("Market Sensitivity Metrics", market_outputs)
    context += format_block("Stability Metrics", stability_outputs)
    context += format_block("Investment Simulation", investment_outputs)

    return context
