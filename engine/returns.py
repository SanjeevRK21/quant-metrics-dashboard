import numpy as np
import pandas as pd

def compute_log_returns(prices: pd.Series) -> pd.Series:
    """
    Compute daily log returns from price series.
    """
    returns = np.log(prices / prices.shift(1))
    return returns.dropna()
