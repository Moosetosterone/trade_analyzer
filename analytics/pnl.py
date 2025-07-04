# FILE: data/pnl.py
from dataclasses import dataclass
from datetime import date
from typing import Dict, List

from matching.matching import MatchRecord


@dataclass
class PnLRecord:
    symbol: str
    date: date
    signal_price: float
    fill_price: float
    quantity: int
    direction: str
    gross_pnl: float
    net_pnl: float


def compute_trade_pnl(
    record: MatchRecord,
    commission_per_contract: float = 0.0,
    slippage_per_contract: float = 0.0,
) -> PnLRecord:
    """
    Turn a matched signal+fill into a PnLRecord.

    :param record: MatchRecord tying signal and fill
    :param commission_per_contract: fee per contract
    :param slippage_per_contract: slippage per contract
    :return: PnLRecord
    """
    qty = record.signal.quantity
    # BUY => side=1, SELL => side=-1
    side = 1 if record.signal.direction.name == "BUY" else -1
    price_diff = (record.fill.fill_price - record.signal.price) * side
    gross = price_diff * qty
    # total fees for all contracts
    fees = (commission_per_contract + slippage_per_contract) * qty
    net = gross - fees
    return PnLRecord(
        symbol=record.signal.symbol,
        date=record.signal.timestamp.date(),
        signal_price=record.signal.price,
        fill_price=record.fill.fill_price,
        quantity=qty,
        direction=record.signal.direction.value,
        gross_pnl=gross,
        net_pnl=net,
    )


def aggregate_daily_pnl(records: List[PnLRecord]) -> Dict[date, Dict[str, float]]:
    """
    Group PnLRecords by trade date and compute daily sum of gross and net P&L.

    Returns a dict: {date: {"gross": X, "net": Y}}
    """
    daily: Dict[date, Dict[str, float]] = {}
    for r in records:
        d = r.date
        if d not in daily:
            daily[d] = {"gross": 0.0, "net": 0.0}
        daily[d]["gross"] += r.gross_pnl
        daily[d]["net"] += r.net_pnl
    return daily
