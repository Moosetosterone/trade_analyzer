# FILE: tests/test_pnl.py
from datetime import date, datetime, timedelta, timezone

import pytest

from analytics.pnl import PnLRecord, aggregate_daily_pnl, compute_trade_pnl
from matching.matching import MatchRecord
from models.schemas import Direction, TradingViewSignal, TradovateFill

# -- Helper functions to build sample MatchRecord


def make_match_record(
    sig_price: float, fill_price: float, qty: int, direction: Direction, ts: datetime
) -> MatchRecord:
    sig = TradingViewSignal(
        alert_id=1,
        raw_ticker="TEST",
        name=None,
        description="{}",
        timestamp=ts,
        symbol="SYM",
        direction=direction,
        price=sig_price,
        quantity=qty,
        order_type=None,
        sentiment=None,
        metadata={},
    )
    fill = TradovateFill(
        order_id="F1",
        account="A1",
        direction=direction,
        contract="SYM",
        filled_qty=qty,
        fill_price=fill_price,
        timestamp=ts + timedelta(seconds=5),
        status="Filled",
        order_type="Market",
        limit_price=None,
        stop_price=None,
        metadata={},
    )
    return MatchRecord(sig, fill)


def test_compute_trade_pnl_buy_with_fees():
    ts = datetime(2025, 7, 5, 12, 0, 0, tzinfo=timezone.utc)
    rec = make_match_record(100.0, 101.0, qty=2, direction=Direction.BUY, ts=ts)
    pnl = compute_trade_pnl(rec, commission_per_contract=2.0, slippage_per_contract=1.0)
    expected_gross = (101.0 - 100.0) * 2
    expected_fees = (2.0 + 1.0) * 2
    expected_net = expected_gross - expected_fees
    assert isinstance(pnl, PnLRecord)
    assert pnl.gross_pnl == pytest.approx(expected_gross)
    assert pnl.net_pnl == pytest.approx(expected_net)
    assert pnl.date == ts.date()


def test_compute_trade_pnl_sell():
    ts = datetime(2025, 7, 6, 9, 30, 0, tzinfo=timezone.utc)
    rec = make_match_record(200.0, 198.0, qty=1, direction=Direction.SELL, ts=ts)
    pnl = compute_trade_pnl(rec)
    # SELL: (198-200)*-1 * 1 = 2
    assert pnl.gross_pnl == pytest.approx(2.0)
    assert pnl.net_pnl == pytest.approx(2.0)


def test_aggregate_daily_pnl_multiple_days():
    # Create PnLRecords for two days
    p1 = PnLRecord(
        "SYM", date(2025, 7, 7), 0, 0, qty := 1, "BUY", gross_pnl=5.0, net_pnl=4.0
    )
    p2 = PnLRecord(
        "SYM", date(2025, 7, 7), 0, 0, qty := 1, "SELL", gross_pnl=-3.0, net_pnl=-3.0
    )
    p3 = PnLRecord(
        "SYM", date(2025, 7, 8), 0, 0, qty := 2, "BUY", gross_pnl=10.0, net_pnl=8.0
    )
    agg = aggregate_daily_pnl([p1, p2, p3])
    assert len(agg) == 2
    assert agg[date(2025, 7, 7)]["gross"] == pytest.approx(2.0)
    assert agg[date(2025, 7, 7)]["net"] == pytest.approx(1.0)
    assert agg[date(2025, 7, 8)]["gross"] == pytest.approx(10.0)
    assert agg[date(2025, 7, 8)]["net"] == pytest.approx(8.0)
