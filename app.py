

import os
import io
import base64
import json
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, jsonify

from engine.data_loader import load_price_data
from engine.returns import compute_log_returns
from engine.growth import total_return, cagr
from engine.risk import annualized_volatility, downside_volatility, max_drawdown
from engine.risk_adjusted import sharpe_ratio, sortino_ratio, calmar_ratio
from engine.tail_risk import skewness, kurtosis_excess, value_at_risk, conditional_value_at_risk
from engine.market import market_metrics
from engine.stability import rolling_sharpe, max_drawdown_duration, recovery_time, drawdown_duration
from engine.drawdown_events import drawdown_events_df
from engine.investment_simulator import simulate_investment

app = Flask(__name__)


def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=100)
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return img_b64


def make_price_chart(prices, ticker):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(prices.index, prices.values, color="#4f8ef7")
    ax.set_title(f"{ticker} Price Series")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price ($)")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig_to_base64(fig)


def make_cumulative_returns_chart(prices, ticker):
    cum = prices / prices.iloc[0]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(cum.index, cum.values, color="#2ecc71")
    ax.set_title(f"{ticker} Cumulative Return (Growth of $1)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Growth of $1")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig_to_base64(fig)


def make_rolling_volatility_chart(returns, ticker):
    rolling_vol = returns.rolling(30).std() * (252 ** 0.5)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(rolling_vol.index, rolling_vol.values, color="#e74c3c")
    ax.set_title(f"{ticker} 30-Day Rolling Annualized Volatility")
    ax.set_xlabel("Date")
    ax.set_ylabel("Volatility")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig_to_base64(fig)


def make_drawdown_chart(prices, ticker):
    peak = prices.cummax()
    drawdown = (prices - peak) / peak
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.fill_between(drawdown.index, drawdown.values, 0, color="#e74c3c", alpha=0.6)
    ax.set_title(f"{ticker} Drawdown")
    ax.set_xlabel("Date")
    ax.set_ylabel("Drawdown (%)")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig_to_base64(fig)


def make_return_distribution_chart(returns, ticker, var_95, cvar_95):
    import numpy as np
    from scipy.stats import gaussian_kde
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(returns, bins=50, density=True, alpha=0.6, color="#4f8ef7", label="Return Distribution")
    kde = gaussian_kde(returns.dropna())
    x = np.linspace(returns.min(), returns.max(), 300)
    ax.plot(x, kde(x), color="orange", lw=2, label="KDE")
    ax.axvline(var_95, color="red", linestyle="--", lw=2, label=f"VaR 95%: {var_95:.2%}")
    ax.axvline(cvar_95, color="darkred", linestyle="-", lw=2, label=f"CVaR 95%: {cvar_95:.2%}")
    ax.set_title(f"{ticker} Return Distribution")
    ax.set_xlabel("Daily Log Return")
    ax.set_ylabel("Density")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig_to_base64(fig)


def make_daily_pnl_chart(portfolio_series, max_gain_date, max_loss_date, ticker):
    daily_pnl = portfolio_series.diff()
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(daily_pnl.index, daily_pnl.values, color="#4f8ef7", alpha=0.7)

    # Highlight extremes
    if max_gain_date in daily_pnl.index:
        ax.scatter(max_gain_date, daily_pnl.loc[max_gain_date], color="#2ecc71", s=100, label="Largest Gain", zorder=5)
    if max_loss_date in daily_pnl.index:
        ax.scatter(max_loss_date, daily_pnl.loc[max_loss_date], color="#e74c3c", s=100, label="Largest Loss", zorder=5)

    ax.axhline(0, color="white", linestyle="--", linewidth=0.8, alpha=0.5)
    ax.set_title(f"Daily P&L (Absolute) ({ticker})")
    ax.set_xlabel("Date")
    ax.set_ylabel("Daily Change ($)")
    ax.legend()
    ax.grid(True, axis="y", alpha=0.2)
    fig.tight_layout()
    return fig_to_base64(fig)


def make_rolling_sharpe_chart(rolling_sharpe_series, ticker):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(rolling_sharpe_series.index, rolling_sharpe_series.values, color="#9b59b6")
    ax.axhline(0, color="gray", linestyle="--", lw=1)
    ax.axhline(1, color="green", linestyle="--", lw=1, alpha=0.7)
    ax.set_title(f"{ticker} 30-Day Rolling Sharpe Ratio")
    ax.set_xlabel("Date")
    ax.set_ylabel("Sharpe Ratio")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig_to_base64(fig)


def make_market_scatter_chart(returns, market_returns, ticker, market_ticker):
    import numpy as np
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.scatter(market_returns, returns, alpha=0.4, s=15, color="#4f8ef7")
    m, b = np.polyfit(market_returns.dropna(), returns.reindex(market_returns.dropna().index).dropna(), 1)
    x_line = np.linspace(market_returns.min(), market_returns.max(), 100)
    ax.plot(x_line, m * x_line + b, color="red", lw=2, label=f"Beta={m:.2f}")
    ax.set_title(f"{ticker} vs {market_ticker}")
    ax.set_xlabel(f"{market_ticker} Returns")
    ax.set_ylabel(f"{ticker} Returns")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig_to_base64(fig)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    ticker = data.get("ticker", "AAPL").upper().strip()
    start_date = data.get("start_date", "2020-01-01")
    end_date = data.get("end_date", "2021-01-01")
    initial_capital = float(data.get("initial_capital", 100000))

    try:
        prices = load_price_data(ticker, start_date, end_date)
        returns = compute_log_returns(prices)

        # Growth
        total_ret = total_return(prices)
        cagr_val = cagr(prices)

        # Risk
        vol = annualized_volatility(returns)
        down_vol = downside_volatility(returns)
        mdd = max_drawdown(prices)

        # Risk-adjusted
        sharpe = sharpe_ratio(returns)
        sortino = sortino_ratio(returns)
        calmar = calmar_ratio(prices)

        # Tail risk
        skew_val = skewness(returns)
        kurt_val = kurtosis_excess(returns)
        var_95 = value_at_risk(returns, 0.95)
        cvar_95 = conditional_value_at_risk(returns, 0.95)

        # Market sensitivity
        market_ticker = "^GSPC"
        market_prices = load_price_data(market_ticker, start_date, end_date)
        market_returns = compute_log_returns(market_prices)
        mkt_stats = market_metrics(returns, market_returns)

        # Stability
        rolling_sharpe_series = rolling_sharpe(returns)
        max_dd_dur = max_drawdown_duration(prices)
        rec_time = recovery_time(prices)

        # Drawdown events
        dd_events = drawdown_events_df(prices)
        dd_table = dd_events.sort_values("drawdown_pct", ascending=False).head(10).to_dict(orient="records")
        for row in dd_table:
            for k, v in row.items():
                if hasattr(v, "isoformat"):
                    row[k] = v.isoformat() if v == v else None
                elif v != v:
                    row[k] = None

        # Investment simulation
        inv_stats = simulate_investment(prices, initial_capital)

        # Charts
        charts = {
            "price": make_price_chart(prices, ticker),
            "cumulative_returns": make_cumulative_returns_chart(prices, ticker),
            "rolling_volatility": make_rolling_volatility_chart(returns, ticker),
            "drawdown": make_drawdown_chart(prices, ticker),
            "return_distribution": make_return_distribution_chart(returns, ticker, var_95, cvar_95),
            "portfolio": make_daily_pnl_chart(inv_stats["portfolio_series"], inv_stats["max_daily_gain_date"], inv_stats["max_daily_loss_date"], ticker),
            "rolling_sharpe": make_rolling_sharpe_chart(rolling_sharpe_series, ticker),
            "market_scatter": make_market_scatter_chart(returns, market_returns, ticker, market_ticker),
        }

        # Extra Drawdown Insights
        worst_dd = dd_events.sort_values("drawdown_pct").iloc[0]
        recent_dd = dd_events.sort_values("trough_date", ascending=False).iloc[0]

        worst_rec = dd_events.dropna(subset=["recovery_time_days"]).sort_values("recovery_time_days", ascending=False).iloc[0] if not dd_events.dropna(subset=["recovery_time_days"]).empty else None
        recent_rec = dd_events.dropna(subset=["recovery_date"]).sort_values("recovery_date", ascending=False).iloc[0] if not dd_events.dropna(subset=["recovery_date"]).empty else None

        def format_dd(ev):
            if ev is None: return None
            return {
                "peak": str(ev["peak_date"].date()),
                "trough": str(ev["trough_date"].date()),
                "pct": f"{ev['drawdown_pct']:.2f}%",
                "recovery": str(ev["recovery_date"].date()) if hasattr(ev["recovery_date"], "date") and not pd.isna(ev["recovery_date"]) else "Ongoing"
            }

        result = {
            "ticker": ticker,
            "start_date": start_date,
            "end_date": end_date,
            "drawdown_insights": {
                "worst_event": format_dd(worst_dd),
                "recent_event": format_dd(recent_dd),
                "worst_recovery": format_dd(worst_rec),
                "recent_recovery": format_dd(recent_rec)
            },
            "growth": {
                "total_return": f"{total_ret:.2%}",
                "cagr": f"{cagr_val:.2%}",
            },
            "risk": {
                "annualized_volatility": f"{vol:.2%}",
                "downside_volatility": f"{down_vol:.2%}",
                "max_drawdown": f"{mdd:.2%}",
            },
            "risk_adjusted": {
                "sharpe_ratio": f"{sharpe:.2f}",
                "sortino_ratio": f"{sortino:.2f}",
                "calmar_ratio": f"{calmar:.2f}",
            },
            "tail_risk": {
                "skewness": f"{skew_val:.2f}",
                "kurtosis": f"{kurt_val:.2f}",
                "var_95": f"{var_95:.2%}",
                "cvar_95": f"{cvar_95:.2%}",
            },
            "market_sensitivity": {
                "beta": f"{mkt_stats['Beta']:.2f}",
                "alpha": f"{mkt_stats['Alpha']:.2%}",
                "r_squared": f"{mkt_stats['R2']:.2f}",
            },
            "stability": {
                "max_drawdown_duration_days": str(max_dd_dur),
                "recovery_time_days": str(rec_time),
            },
            "investment": {
                "initial": f"${initial_capital:,.2f}",
                "final": f"${inv_stats['final_value']:,.2f}",
                "min_value": f"${inv_stats['min_value']:,.2f}",
                "min_value_date": str(inv_stats['min_value_date'].date()),
                "max_value": f"${inv_stats['max_value']:,.2f}",
                "max_value_date": str(inv_stats['max_value_date'].date()),
            },
            "drawdown_events": dd_table,
            "charts": charts,
        }

        return jsonify({"success": True, "data": result})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    context = data.get("context", {})
    question = data.get("question", "")

    if not question:
        return jsonify({"success": False, "error": "No question provided"}), 400

    try:
        from chat.research_chatbot import research_bot
        response = research_bot(context, question)
        return jsonify({"success": True, "response": response})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run()
