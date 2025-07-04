# FILE: tests/test_analytics.py
from datetime import datetime, timezone

import pytest

from analytics.analytics import SlippageRecord, aggregate_slippage, compute_slippage
from matching.matching import MatchRecord
from models.schemas import Direction, TradingViewSignal, TradovateFill

# Helpers to build sample match records


def make_signal(price, ts):
    return TradingViewSignal(
        alert_id=0,
        raw_ticker="X",
        name=None,
        description="{}",
        timestamp=ts,
        symbol="SYM",
        direction=Direction.BUY,
        price=price,
        quantity=1,
        order_type=None,
        sentiment=None,
        metadata={},
    )


def make_fill(price, ts):
    return TradovateFill(
        order_id="F",
        account="A",
        direction=Direction.BUY,
        contract="SYM",
        filled_qty=1,
        fill_price=price,
        timestamp=ts,
        status="Filled",
        order_type="Mkt",
        limit_price=None,
        stop_price=None,
        metadata={},
    )


def test_compute_slippage_buy():
    sig_ts = datetime(2025, 7, 4, 12, 0, 0, tzinfo=timezone.utc)
    fill_ts = datetime(2025, 7, 4, 12, 0, 5, tzinfo=timezone.utc)
    sig = make_signal(100.0, sig_ts)
    fill = make_fill(100.5, fill_ts)
    rec = MatchRecord(sig, fill)
    slip = compute_slippage(rec, tick_size=0.25, tick_value=10.0)
    assert isinstance(slip, SlippageRecord)
    assert slip.slippage_ticks == pytest.approx((100.5 - 100.0) / 0.25)
    assert slip.slippage_dollars == pytest.approx(slip.slippage_ticks * 10.0)


def test_compute_slippage_sell():
    sig_ts = datetime(2025, 7, 4, 12, 0, 0, tzinfo=timezone.utc)
    fill_ts = datetime(2025, 7, 4, 12, 0, 5, tzinfo=timezone.utc)
    # for SELL, price diff inverted
    sig = make_signal(100.0, sig_ts)
    sig.direction = Direction.SELL
    fill = make_fill(99.5, fill_ts)
    fill.direction = Direction.SELL
    rec = MatchRecord(sig, fill)
    slip = compute_slippage(rec, tick_size=0.5, tick_value=5.0)
    # (99.5-100.0)*-1 = +0.5 /0.5 = 1 tick →
    assert slip.slippage_ticks == pytest.approx(1.0)
    assert slip.slippage_dollars == pytest.approx(5.0)


def test_aggregate_slippage():
    r1 = SlippageRecord(
        "SYM", datetime.now(), datetime.now(), slippage_ticks=1, slippage_dollars=10
    )
    r2 = SlippageRecord(
        "SYM", datetime.now(), datetime.now(), slippage_ticks=3, slippage_dollars=30
    )
    agg = aggregate_slippage([r1, r2])
    assert agg["count"] == 2
    assert agg["mean_ticks"] == pytest.approx(2.0)
    assert agg["median_dollars"] == pytest.approx(20.0)
    assert agg["max_ticks"] == 3
    assert agg["min_dollars"] == 10
