# --------------------------------------
# FILE: tests/test_db.py
# --------------------------------------
from datetime import datetime, timezone

import pytest
from sqlmodel import select

from data.db import (
    Fill,
    Instrument,
    Signal,
    get_session,
    init_db,
    insert_fill,
    insert_signal,
)
from data.schemas import Direction, TradingViewSignal, TradovateFill


@pytest.fixture
def engine(tmp_path):
    db_file = tmp_path / "test_trades.db"
    url = f"sqlite:///{db_file}"
    engine = init_db(db_url=url)
    yield engine


@pytest.fixture
def session(engine):
    return get_session(engine)


@pytest.fixture
def sample_signal():
    return TradingViewSignal(
        alert_id=1,
        raw_ticker="DUMMY",
        name=None,
        description="{}",
        timestamp=datetime.now(timezone.utc),
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
        order_id="F1",
        account="ACC",
        direction=Direction.SELL,
        contract="MESM25",
        filled_qty=2,
        fill_price=101.0,
        timestamp=datetime.now(timezone.utc),
        status="Filled",
        order_type="Market",
        limit_price=None,
        stop_price=None,
        metadata={},
    )


def test_insert_signal_and_instrument(session, sample_signal):
    rec = insert_signal(session, sample_signal)
    assert rec.id is not None
    inst = session.exec(select(Instrument).where(Instrument.symbol == "MESM25")).first()
    assert inst is not None and inst.symbol == "MESM25"
    signals = session.exec(select(Signal)).all()
    assert len(signals) == 1


def test_insert_fill_and_instrument(session, sample_fill):
    rec = insert_fill(session, sample_fill)
    assert rec.id is not None
    inst = session.exec(select(Instrument).where(Instrument.symbol == "MESM25")).first()
    assert inst is not None and inst.symbol == "MESM25"
    fills = session.exec(select(Fill)).all()
    assert len(fills) == 1
