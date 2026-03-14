import numpy as np
import pandas as pd


def annualized_volatility(returns: pd.Series, trading_days: int = 252) -> float:
    """
    Compute annualized volatility from daily returns. here annual volatility mean it takes the daily 
    returns of your entire timeline and shrinks it down to 1 year.
    """
    if returns.empty:
        raise ValueError("Return series is empty")

    return returns.std() * np.sqrt(trading_days)


def downside_volatility(returns: pd.Series, trading_days: int = 252) -> float:
    """
    Compute downside volatility (negative returns only) for the entire dataset like when volatility
    occurs what percent of it is downwards out of 100.
    """
    if returns.empty:
        raise ValueError("Return series is empty")

    downside_returns = returns[returns < 0]

    if downside_returns.empty:
        return 0.0

    return downside_returns.std() * np.sqrt(trading_days)


def max_drawdown(prices: pd.Series) -> float:
    """
    Compute maximum drawdown from price series for the entire dataset.
    """
    if prices.empty:
        raise ValueError("Price series is empty")

    cumulative_max = prices.cummax()
    drawdowns = (prices - cumulative_max) / cumulative_max

    return drawdowns.min()
