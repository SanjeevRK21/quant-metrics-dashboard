import numpy as np
import pandas as pd
from scipy.stats import linregress


def market_metrics(
    stock_returns: pd.Series,
    market_returns: pd.Series,
    trading_days: int = 252
) -> dict:
    """
    Compute Beta, Alpha, and R-squared using linear regression.
    """

    # Align dates
    data = pd.concat([stock_returns, market_returns], axis=1).dropna()
    data.columns = ["stock", "market"]

    if data.empty:
        raise ValueError("No overlapping data between stock and market returns.")

    regression = linregress(data["market"], data["stock"])

    beta = regression.slope
    alpha_daily = regression.intercept
    r_squared = regression.rvalue ** 2

    # Annualize alpha
    alpha_annual = alpha_daily * trading_days

    return {
        "Beta": beta,
        "Alpha": alpha_annual,
        "R2": r_squared
    }
