import pandas as pd

def total_return(prices: pd.Series) -> float:
    """
    Compute total return over the entire period.
    """
    if prices.empty:
        raise ValueError("Price series is empty")

    start_price = prices.iloc[0]
    end_price = prices.iloc[-1]

    return (end_price / start_price) - 1


def cagr(prices: pd.Series) -> float:
    """
    Compute Compound Annual Growth Rate (CAGR).
    """
    if prices.empty:
        raise ValueError("Price series is empty")

    start_price = prices.iloc[0]
    end_price = prices.iloc[-1]

    start_date = prices.index[0]
    end_date = prices.index[-1]

    num_years = (end_date - start_date).days / 365.25

    if num_years <= 0:
        raise ValueError("Date range too short for CAGR calculation")

    return (end_price / start_price) ** (1 / num_years) - 1
