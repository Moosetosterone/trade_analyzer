# FILE: tests/test_summary.py
from datetime import date

import pytest

from data.pnl import PnLRecord
from data.summary import equity_curve, expectancy, max_drawdown, win_rate


@pytest.fixture
def sample_pnl():
    # create PnLRecords for three days
    return [
        PnLRecord("SYM", date(2025, 1, 1), 0, 0, 1, "BUY", gross_pnl=5, net_pnl=4),
        PnLRecord("SYM", date(2025, 1, 2), 0, 0, 1, "BUY", gross_pnl=-3, net_pnl=-4),
        PnLRecord("SYM", date(2025, 1, 3), 0, 0, 1, "BUY", gross_pnl=2, net_pnl=1),
    ]


def test_win_rate(sample_pnl):
    assert win_rate(sample_pnl) == pytest.approx(2 / 3)
    assert win_rate([]) == 0.0


def test_expectancy(sample_pnl):
    # (4 + -4 + 1) / 3 = 0.333...
    assert expectancy(sample_pnl) == pytest.approx((4 - 4 + 1) / 3)
    assert expectancy([]) == 0.0


def test_equity_curve_and_drawdown(sample_pnl):
    curve = equity_curve(sample_pnl)
    # cumulative: day1=4, day2=4-4=0, day3=0+1=1
    expected = [
        (date(2025, 1, 1), 4.0),
        (date(2025, 1, 2), 0.0),
        (date(2025, 1, 3), 1.0),
    ]
    assert curve == expected
    # max drawdown from peak=4 to trough=0 = 4
    assert max_drawdown(curve) == pytest.approx(4.0)
