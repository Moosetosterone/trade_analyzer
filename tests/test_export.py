import csv
import os
from datetime import date

import pytest

from data.export import export_daily_summary, export_pnl_records
from data.pnl import PnLRecord


@pytest.fixture
def tmp_csv(tmp_path):
    return tmp_path / "test.csv"


def test_export_pnl_records(tmp_csv):
    records = [
        PnLRecord(
            "SYM", date(2025, 1, 1), 100, 101, 1, "BUY", gross_pnl=1.0, net_pnl=0.5
        ),
        PnLRecord(
            "FUT", date(2025, 1, 2), 200, 198, 2, "SELL", gross_pnl=4.0, net_pnl=3.0
        ),
    ]
    export_pnl_records(records, str(tmp_csv))
    # Read back and verify rows
    with open(tmp_csv, newline="") as f:
        reader = list(csv.DictReader(f))
    assert len(reader) == 2
    assert reader[0]["symbol"] == "SYM"
    assert reader[1]["direction"] == "SELL"
    assert float(reader[1]["net_pnl"]) == pytest.approx(3.0)


def test_export_daily_summary(tmp_csv):
    summary = {
        date(2025, 1, 1): {"gross": 5.0, "net": 4.5},
        date(2025, 1, 2): {"gross": -2.0, "net": -2.0},
    }
    export_daily_summary(summary, str(tmp_csv))
    with open(tmp_csv, newline="") as f:
        reader = {row["date"]: row for row in csv.DictReader(f)}
    assert "2025-01-01" in reader
    assert float(reader["2025-01-01"]["gross_pnl"]) == pytest.approx(5.0)
    assert float(reader["2025-01-02"]["net_pnl"]) == pytest.approx(-2.0)
