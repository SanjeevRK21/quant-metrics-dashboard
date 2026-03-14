# chat/event_explainer.py

from llm.ollama_client import call_llm
from chat.prompts import (
    risk_metrics_prompt,  
    risk_adjusted_metrics_prompt,
    tail_risk_metrics_prompt,
    market_sensitivity_prompt,
    stability_metrics_prompt,
    drawdown_event_prompt,
    investment_simulation_prompt

)



def explain_event_with_llm(
    ticker: str,
    start_date: str,
    end_date: str,
    event_name: str,
    event_outputs: dict
) -> str:
    """
    Route event data to the correct prompt template and
    return an LLM-generated explanation.

    Parameters
    ----------
    ticker : str
        Stock ticker symbol
    start_date : str
        Analysis start date
    end_date : str
        Analysis end date
    event_name : str
        Name of the analysis event
    event_outputs : dict
        Computed metrics or event-level outputs (already formatted)

    Returns
    -------
    str
        LLM-generated explanation text
    """

    # -------------------------
    # Select prompt template
    # -------------------------
    if event_name == "Risk Metrics":
        prompt = risk_metrics_prompt(
            ticker, start_date, end_date, event_outputs
        )

    elif event_name == "Risk-Adjusted Metrics":
        prompt = risk_adjusted_metrics_prompt(
            ticker, start_date, end_date, event_outputs
        )

    elif event_name == "Tail Risk Metrics":
        prompt = tail_risk_metrics_prompt(
            ticker, start_date, end_date, event_outputs
        )

    elif event_name == "Market Sensitivity Metrics":
        prompt = market_sensitivity_prompt(
            ticker, start_date, end_date, event_outputs
        )

    elif event_name == "Stability Metrics":
        prompt = stability_metrics_prompt(
            ticker, start_date, end_date, event_outputs
        )

    elif event_name in {
        "Drawdown Event",
        "Worst Drawdown Event",
        "Most Recent Drawdown Event",
        "Worst Recovery Event",
        "Most Recent Recovery Event"
    }:
        prompt = drawdown_event_prompt(
            ticker, start_date, end_date, event_outputs
        )

    elif event_name == "Investment Simulation":
        prompt = investment_simulation_prompt(
            ticker, start_date, end_date, event_outputs
        )

    elif event_name == "Growth Metrics":
        prompt = investment_simulation_prompt(
            ticker, start_date, end_date, event_outputs
        )

    else:
        raise ValueError(
            f"No prompt template defined for event_name='{event_name}'"
        )

    # -------------------------
    # Call LLM
    # -------------------------
    response = call_llm(prompt)

    return response.strip()
