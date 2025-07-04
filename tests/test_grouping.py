from datetime import date

import pytest

from data.grouping import (
    filter_by_date_range,
    group_by,
    group_by_date,
    group_by_instrument,
)
from data.pnl import PnLRecord


# Helper to create a generic record with symbol and date attributes
class Dummy:
    def __init__(self, symbol, d):
        self.symbol = symbol
        self.date = d


@pytest.fixture
def sample_records():
    return [
        Dummy("A", date(2025, 1, 1)),
        Dummy("B", date(2025, 1, 2)),
        Dummy("A", date(2025, 1, 3)),
        Dummy("C", date(2025, 1, 2)),
    ]


def test_group_by_generic(sample_records):
    # group by symbol
    grouped = group_by(sample_records, lambda r: r.symbol)
    assert set(grouped.keys()) == {"A", "B", "C"}
    assert len(grouped["A"]) == 2


def test_group_by_instrument(sample_records):
    grouped = group_by_instrument(sample_records)
    assert set(grouped.keys()) == {"A", "B", "C"}


def test_group_by_date(sample_records):
    grouped = group_by_date(sample_records)
    assert set(grouped.keys()) == {date(2025, 1, 1), date(2025, 1, 2), date(2025, 1, 3)}
    assert len(grouped[date(2025, 1, 2)]) == 2


def test_filter_by_date_range(sample_records):
    filtered = filter_by_date_range(
        sample_records, start_date=date(2025, 1, 2), end_date=date(2025, 1, 3)
    )
    # should include records with date 1/2 and 1/3
    assert all(
        r.date >= date(2025, 1, 2) and r.date <= date(2025, 1, 3) for r in filtered
    )
    assert len(filtered) == 3
