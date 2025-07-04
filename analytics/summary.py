# FILE: data/summary.py
from datetime import date
from typing import Dict, List, Tuple

from analytics.pnl import PnLRecord


def win_rate(records: List[PnLRecord]) -> float:
    """
    Calculate win rate: percentage of trades with positive net P&L.
    Returns a float between 0 and 1.
    """
    if not records:
        return 0.0
    wins = sum(1 for r in records if r.net_pnl > 0)
    return wins / len(records)


def expectancy(records: List[PnLRecord]) -> float:
    """
    Calculate expectancy: average net P&L per trade.
    """
    if not records:
        return 0.0
    total = sum(r.net_pnl for r in records)
    return total / len(records)


def equity_curve(records: List[PnLRecord]) -> List[Tuple[date, float]]:
    """
    Build an equity curve: cumulative net P&L by trade date.
    Returns a sorted list of (date, cumulative_net_pnl).
    """
    # aggregate daily net
    daily: Dict[date, float] = {}
    for r in records:
        daily.setdefault(r.date, 0.0)
        daily[r.date] += r.net_pnl
    # sort dates
    sorted_dates = sorted(daily)
    cum = 0.0
    curve: List[Tuple[date, float]] = []
    for d in sorted_dates:
        cum += daily[d]
        curve.append((d, cum))
    return curve


def max_drawdown(curve: List[Tuple[date, float]]) -> float:
    """
    Compute maximum drawdown from an equity curve.
    Drawdown is defined as the maximum peak-to-trough decline.
    Returns the drawdown amount (positive value).
    """
    max_dd = 0.0
    peak = float("-inf")
    for _, value in curve:
        if value > peak:
            peak = value
        dd = peak - value
        if dd > max_dd:
            max_dd = dd
    return max_dd
