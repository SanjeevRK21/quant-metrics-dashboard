# engine/investment_simulator.py

import pandas as pd
from typing import Dict


def simulate_investment(
    prices: pd.Series,
    initial_investment: float
) -> Dict:
    """
    Simulate investment value over time given an initial investment.

    Returns final value, min/max value with dates,
    and largest single-day gain/loss with dates.
    """

    # Normalize prices to start at 1
    normalized_prices = prices / prices.iloc[0]

    # Capital over time
    portfolio_value = initial_investment * normalized_prices

    # Daily changes in capital
    daily_change = portfolio_value.diff()

    # Final value
    final_value = portfolio_value.iloc[-1]

    # Min / Max portfolio value
    min_value = portfolio_value.min()
    min_value_date = portfolio_value.idxmin()

    max_value = portfolio_value.max()
    max_value_date = portfolio_value.idxmax()

    # Largest single-day gain
    max_gain = daily_change.max()
    max_gain_date = daily_change.idxmax()

    # Largest single-day loss
    max_loss = daily_change.min()
    max_loss_date = daily_change.idxmin()

    return {
        "initial_investment": initial_investment,
        "final_value": final_value,

        "min_value": min_value,
        "min_value_date": min_value_date,

        "max_value": max_value,
        "max_value_date": max_value_date,

        "max_daily_gain": max_gain,
        "max_daily_gain_date": max_gain_date,

        "max_daily_loss": max_loss,
        "max_daily_loss_date": max_loss_date,

        "portfolio_series": portfolio_value
    }
