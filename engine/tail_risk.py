import numpy as np
import pandas as pd
from scipy.stats import skew, kurtosis


def skewness(returns: pd.Series) -> float:
    """
    Compute skewness of returns.
    """
    if returns.empty:
        raise ValueError("Return series is empty")

    return skew(returns)


def kurtosis_excess(returns: pd.Series) -> float:
    """
    Compute excess kurtosis (fat tails).
    """
    if returns.empty:
        raise ValueError("Return series is empty")

    return kurtosis(returns, fisher=True)


def value_at_risk(
    returns: pd.Series,
    confidence_level: float = 0.95
) -> float:
    """
    Historical Value at Risk (VaR).
    """
    if returns.empty:
        raise ValueError("Return series is empty")

    return np.percentile(returns, (1 - confidence_level) * 100)


def conditional_value_at_risk(
    returns: pd.Series,
    confidence_level: float = 0.95
) -> float:
    """
    Conditional Value at Risk (CVaR / Expected Shortfall).
    """
    var = value_at_risk(returns, confidence_level)
    return returns[returns <= var].mean()
