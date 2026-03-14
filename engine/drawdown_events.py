# engine/drawdown_events.py

import pandas as pd
from typing import List, Dict


def extract_drawdown_events(prices: pd.Series) -> List[Dict]:
    """
    Extract drawdown and recovery episodes from a price series.

    Each episode contains:
    - peak_date
    - trough_date
    - recovery_date (None if ongoing)
    - drawdown_pct
    - drawdown_duration (days) 
    - recovery_time (days or None)
    """

    events = []

    peak_price = prices.iloc[0]
    peak_date = prices.index[0]

    trough_price = peak_price
    trough_date = peak_date

    in_drawdown = False

    for date, price in prices.items():

        # New peak → recovery or reset
        if price >= peak_price:

            if in_drawdown:
                events.append({
                    "peak_date": peak_date,
                    "trough_date": trough_date,
                    "recovery_date": date,
                    "drawdown_pct": (trough_price - peak_price) / peak_price,
                    "drawdown_duration_days": (trough_date - peak_date).days,
                    "recovery_time_days": (date - trough_date).days
                })
                in_drawdown = False

            peak_price = price
            peak_date = date
            trough_price = price
            trough_date = date

        else:
            # Still underwater
            in_drawdown = True

            if price < trough_price:
                trough_price = price
                trough_date = date

    # Handle ongoing drawdown
    if in_drawdown:
        events.append({
            "peak_date": peak_date,
            "trough_date": trough_date,
            "recovery_date": None,
            "drawdown_pct": (trough_price - peak_price) / peak_price,
            "drawdown_duration_days": (trough_date - peak_date).days,
            "recovery_time_days": None
        })

    return events


def drawdown_events_df(prices: pd.Series) -> pd.DataFrame:
    """
    Return drawdown events as a DataFrame.
    """
    df = pd.DataFrame(extract_drawdown_events(prices))

    if not df.empty:
        df["drawdown_pct"] = df["drawdown_pct"] * 100

    return df
