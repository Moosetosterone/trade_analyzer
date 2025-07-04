# FILE: data/analytics.py
from dataclasses import dataclass
from datetime import datetime
from statistics import mean, median
from typing import Dict, List

from matching.matching import MatchRecord
from models.schemas import Direction


@dataclass
class SlippageRecord:
    symbol: str
    signal_timestamp: datetime
    fill_timestamp: datetime
    slippage_ticks: float
    slippage_dollars: float


def compute_slippage(
    record: MatchRecord, tick_size: float, tick_value: float
) -> SlippageRecord:
    """
    Compute slippage for a matched signal and fill.
    :param record: MatchRecord tying signal and fill
    :param tick_size: price increment per tick (e.g. 0.25)
    :param tick_value: dollar value per tick (e.g. 12.5)
    :return: SlippageRecord with ticks and dollar slippage
    """
    direction = 1 if record.signal.direction == Direction.BUY else -1
    price_diff = (record.fill.fill_price - record.signal.price) * direction
    ticks = price_diff / tick_size
    dollars = ticks * tick_value
    return SlippageRecord(
        symbol=record.signal.symbol,
        signal_timestamp=record.signal.timestamp,
        fill_timestamp=record.fill.timestamp,
        slippage_ticks=ticks,
        slippage_dollars=dollars,
    )


def aggregate_slippage(records: List[SlippageRecord]) -> Dict[str, float]:
    """
    Aggregate a list of SlippageRecords into summary statistics.
    Returns dict with count, mean/median/min/max for ticks and dollars.
    """
    ticks_list = [r.slippage_ticks for r in records]
    dollars_list = [r.slippage_dollars for r in records]
    return {
        "count": len(records),
        "mean_ticks": mean(ticks_list) if ticks_list else 0.0,
        "median_ticks": median(ticks_list) if ticks_list else 0.0,
        "max_ticks": max(ticks_list) if ticks_list else 0.0,
        "min_ticks": min(ticks_list) if ticks_list else 0.0,
        "mean_dollars": mean(dollars_list) if dollars_list else 0.0,
        "median_dollars": median(dollars_list) if dollars_list else 0.0,
        "max_dollars": max(dollars_list) if dollars_list else 0.0,
        "min_dollars": min(dollars_list) if dollars_list else 0.0,
    }
