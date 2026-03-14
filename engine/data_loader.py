import yfinance as yf
import pandas as pd
from typing import Tuple


def get_available_date_range(ticker: str) -> Tuple[pd.Timestamp, pd.Timestamp]:
    """
    Fetch the full available date range for a given ticker from Yahoo Finance.
    """
    data = yf.download(ticker, period="max", progress=False)

    if data.empty:
        raise ValueError("No data found for this ticker.")

    start_date = data.index.min()
    end_date = data.index.max()

    return start_date, end_date


def load_price_data(ticker: str, start: str, end: str) -> pd.Series:
    """
    Load adjusted (auto-adjusted) close prices for a given ticker and date range.
    """
    data = yf.download(ticker, start=start, end=end, progress=False)

    if data.empty:
        raise ValueError("No data fetched. Check date range.")

    prices = data["Close"].dropna().squeeze()
    return prices
