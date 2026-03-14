import numpy as np
import pandas as pd


def rolling_sharpe(
    returns: pd.Series,
    window: int = 30,
    trading_days: int = 252
) -> pd.Series:
    """
    Compute rolling Sharpe ratio.
    """
    rolling_mean = returns.rolling(window).mean() * trading_days
    rolling_std = returns.rolling(window).std() * np.sqrt(trading_days)
    return rolling_mean / rolling_std


def drawdown_series(prices: pd.Series) -> pd.Series:
    """
    Compute drawdown series.
    """
    cumulative_max = prices.cummax()
    return (prices - cumulative_max) / cumulative_max


def drawdown_duration(prices: pd.Series) -> pd.Series:
    """
    Compute drawdown duration (time spent underwater).
    """
    dd = drawdown_series(prices)
    duration = np.zeros(len(dd))
    for i in range(1, len(dd)):
        if dd.iloc[i] < 0:
            duration[i] = duration[i - 1] + 1
        else:
            duration[i] = 0
    return pd.Series(duration, index=dd.index)


def max_drawdown_duration(prices: pd.Series) -> int:
    """
    Maximum drawdown duration.
    """
    duration = drawdown_duration(prices)
    return int(duration.max())


def recovery_time(prices: pd.Series) -> int:
    """
    Time taken to recover from maximum drawdown.
    """
    dd = drawdown_series(prices)
    trough_date = dd.idxmin()
    peak_before = prices.loc[:trough_date].idxmax()

    recovery_prices = prices.loc[trough_date:]
    recovered = recovery_prices[recovery_prices >= prices.loc[peak_before]]

    if recovered.empty:
        return -1  # Not yet recovered

    recovery_date = recovered.index[0]
    return (recovery_date - trough_date).days
