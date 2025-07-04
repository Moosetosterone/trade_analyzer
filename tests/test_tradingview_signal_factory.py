# tests/test_tradingview_signal_factory.py

import json
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from models.schemas import Direction
from normalization.normalizer import TradingViewSignalFactory


@pytest.fixture
def sample_row():
    return {
        "Alert ID": "42",
        "Ticker": "MES1!",
        "Name": "MyTestAlert",
        "Description": json.dumps(
            {
                "ticker": "MES1!",
                "action": "buy",
                "price": "4100.5",
                "quantity": "2",
                "orderType": "Market",
                "sentiment": "bull",
            }
        ),
        "Time": "2025-07-03 14:30:00",
    }


def test_factory_parses_core_fields(sample_row):
    sig = TradingViewSignalFactory.from_csv_row(sample_row.copy())
    # ensure timestamp is UTC-aware
    assert sig.timestamp == datetime(2025, 7, 3, 14, 30, 0, tzinfo=ZoneInfo("UTC"))
    assert sig.symbol == "MES1!"
    assert sig.direction == Direction.BUY
    assert sig.price == 4100.5
    assert sig.quantity == 2


def test_factory_stashes_extras(sample_row):
    sig = TradingViewSignalFactory.from_csv_row(sample_row.copy())
    assert sig.order_type == "Market"
    assert sig.sentiment == "bull"
    assert "time" not in sig.metadata
