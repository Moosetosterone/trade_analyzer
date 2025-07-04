# tests/test_matching_engine.py

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest

from matching.matching import MatchingEngine, MatchRecord
from models.schemas import Direction, TradingViewSignal, TradovateFill

UTC = ZoneInfo("UTC")


@pytest.fixture
def sample_signal():
    return TradingViewSignal(
        alert_id=1,
        raw_ticker="DUMMY",
        name=None,
        description="",
        timestamp=datetime(2025, 7, 3, 14, 0, 0, tzinfo=UTC),
        symbol="MESM25",
        direction=Direction.BUY,
        price=100.0,
        quantity=1,
        order_type=None,
        sentiment=None,
        metadata={},
    )


@pytest.fixture
def sample_fill():
    return TradovateFill(
        order_id="FILL1",
        account="DemoAcct",
        direction=Direction.BUY,
        contract="MESM25",
        filled_qty=1,
        fill_price=100.5,
        timestamp=datetime(2025, 7, 3, 14, 1, 0, tzinfo=UTC),
        status="Filled",
        order_type="Market",
        limit_price=None,
        stop_price=None,
        metadata={},
    )


def test_match_within_tolerance(sample_signal, sample_fill):
    engine = MatchingEngine(tolerance=timedelta(minutes=2))
    matches = engine.match([sample_signal], [sample_fill])
    assert len(matches) == 1
    rec = matches[0]
    assert isinstance(rec, MatchRecord)
    assert rec.signal is sample_signal
    assert rec.fill is sample_fill


def test_no_match_outside_tolerance(sample_signal, sample_fill):
    sample_fill.timestamp = sample_fill.timestamp + timedelta(minutes=5)
    engine = MatchingEngine(tolerance=timedelta(minutes=2))
    matches = engine.match([sample_signal], [sample_fill])
    assert matches == []


def test_multiple_signals_and_fills(sample_signal, sample_fill):
    # second signal/fill pair
    sig2 = TradingViewSignal(
        alert_id=2,
        raw_ticker="DUMMY",
        name=None,
        description="",
        timestamp=datetime(2025, 7, 3, 14, 5, 0, tzinfo=UTC),
        symbol="MESM25",
        direction=Direction.BUY,
        price=101.0,
        quantity=1,
        order_type=None,
        sentiment=None,
        metadata={},
    )
    fill2 = TradovateFill(
        order_id="FILL2",
        account="DemoAcct",
        direction=Direction.BUY,
        contract="MESM25",
        filled_qty=1,
        fill_price=101.5,
        timestamp=datetime(2025, 7, 3, 14, 6, 0, tzinfo=UTC),
        status="Filled",
        order_type="Market",
        limit_price=None,
        stop_price=None,
        metadata={},
    )

    engine = MatchingEngine(tolerance=timedelta(minutes=2))
    matches = engine.match([sample_signal, sig2], [sample_fill, fill2])
    assert len(matches) == 2
    assert matches[0].signal is sample_signal
    assert matches[0].fill is sample_fill
    assert matches[1].signal is sig2
    assert matches[1].fill is fill2


def test_fill_not_reused(sample_signal, sample_fill):
    # two signals but only one fill available
    sig2 = TradingViewSignal(
        alert_id=2,
        raw_ticker="DUMMY",
        name=None,
        description="",
        timestamp=datetime(2025, 7, 3, 14, 1, 30, tzinfo=UTC),  # still within 2m
        symbol="MESM25",
        direction=Direction.BUY,
        price=100.2,
        quantity=1,
        order_type=None,
        sentiment=None,
        metadata={},
    )

    engine = MatchingEngine(tolerance=timedelta(minutes=2))
    matches = engine.match([sample_signal, sig2], [sample_fill])
    # Only the first signal gets matched, then fill is consumed
    assert len(matches) == 1
    assert matches[0].signal is sample_signal
    assert matches[0].fill is sample_fill
