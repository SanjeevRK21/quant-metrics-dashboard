import numpy as np
import pandas as pd
from engine.risk import annualized_volatility, downside_volatility, max_drawdown
from engine.growth import cagr


def sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.0,
    trading_days: int = 252
) -> float:
    """
    Compute annualized Sharpe Ratio.
    """
    if returns.empty:
        raise ValueError("Return series is empty")

    annual_return = returns.mean() * trading_days
    vol = annualized_volatility(returns, trading_days)

    if vol == 0:
        return np.nan

    return (annual_return - risk_free_rate) / vol


def sortino_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.0,
    trading_days: int = 252
) -> float:
    """
    Compute annualized Sortino Ratio.
    """
    if returns.empty:
        raise ValueError("Return series is empty")

    annual_return = returns.mean() * trading_days
    down_vol = downside_volatility(returns, trading_days)

    if down_vol == 0:
        return np.nan

    return (annual_return - risk_free_rate) / down_vol


def calmar_ratio(prices: pd.Series) -> float:
    """
    Compute Calmar Ratio = CAGR / |Max Drawdown|
    """
    mdd = max_drawdown(prices)

    if mdd == 0:
        return np.nan

    return cagr(prices) / abs(mdd)
