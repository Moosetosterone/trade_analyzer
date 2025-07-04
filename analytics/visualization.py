from datetime import date
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import DateFormatter
from matplotlib.figure import Figure


def plot_equity_curve(
    curve: List[Tuple[date, float]], title: str = "Equity Curve"
) -> plt.Figure:
    """
    Plot an equity curve given a list of (date, cumulative_net_pnl).

    Args:
        curve: List of tuples (date, cumulative P&L) sorted by date.
        title: Chart title.

    Returns:
        Matplotlib Figure object.
    """
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Cumulative P&L")
    ax.grid(True)

    # only plot if we have data
    if curve:
        dates, values = zip(*curve)
        ax.plot(dates, values)

    fig.autofmt_xdate()
    fig.tight_layout()
    return fig


def plot_slippage_histogram(
    slippages: List[float], bins: int = 20, title: str = "Slippage Distribution"
) -> plt.Figure:
    """
    Plot a histogram of slippage values.

    Args:
        slippages: List of slippage values (e.g. ticks or dollars).
        bins:      Number of histogram bins.
        title:     Chart title.

    Returns:
        Matplotlib Figure object.
    """
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel("Slippage")
    ax.set_ylabel("Frequency")
    ax.grid(True)

    # only plot if we have slippage data
    if slippages:
        ax.hist(slippages, bins=bins, edgecolor="black")

    fig.tight_layout()
    return fig


def plot_equity_and_drawdown(
    curve: List[Tuple[date, float]],
    title: str = "Equity & Drawdown",
    equity_color: str = "#00bfbf",  # teal
    drawdown_color: str = "#800080",  # purple
    drawdown_alpha: float = 0.3,
) -> Figure:
    """
    Plot an equity curve (filled) and highlight drawdown periods.
    """
    fig, ax = plt.subplots()
    if not curve:
        ax.set_title(title)
        return fig

    dates, equity = zip(*curve)
    equity = np.array(equity)
    # compute running peak
    peaks = np.maximum.accumulate(equity)
    # fill under equity line
    ax.fill_between(
        dates,
        equity,
        equity[0],
        where=equity >= equity[0],
        color=equity_color,
        alpha=0.1,
    )
    ax.plot(dates, equity, color=equity_color, linewidth=2)

    # shade drawdown regions
    ax.fill_between(
        dates,
        equity,
        peaks,
        where=equity < peaks,
        color=drawdown_color,
        alpha=drawdown_alpha,
    )

    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Equity / Drawdown")
    ax.grid(True, linestyle="--", alpha=0.5)
    fig.autofmt_xdate()
    fig.tight_layout()
    return fig
