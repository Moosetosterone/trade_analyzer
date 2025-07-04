# FILE: data/export.py
import csv
from datetime import date
from typing import Dict, List, Union

from analytics.pnl import PnLRecord


def export_pnl_records(pnl_records: List[PnLRecord], filepath: str) -> None:
    """
    Export a list of PnLRecord to a CSV file.

    Columns: symbol, date, direction, quantity, signal_price, fill_price, gross_pnl, net_pnl
    """
    fieldnames = [
        "symbol",
        "date",
        "direction",
        "quantity",
        "signal_price",
        "fill_price",
        "gross_pnl",
        "net_pnl",
    ]
    with open(filepath, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for rec in pnl_records:
            writer.writerow(
                {
                    "symbol": rec.symbol,
                    "date": rec.date.isoformat(),
                    "direction": rec.direction,
                    "quantity": rec.quantity,
                    "signal_price": rec.signal_price,
                    "fill_price": rec.fill_price,
                    "gross_pnl": rec.gross_pnl,
                    "net_pnl": rec.net_pnl,
                }
            )


def export_daily_summary(
    daily_summary: Dict[date, Dict[str, float]], filepath: str
) -> None:
    """
    Export a daily summary dict to CSV.

    Columns: date, gross_pnl, net_pnl
    """
    fieldnames = ["date", "gross_pnl", "net_pnl"]
    with open(filepath, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for d, vals in sorted(daily_summary.items()):
            writer.writerow(
                {
                    "date": d.isoformat(),
                    "gross_pnl": vals.get("gross", 0.0),
                    "net_pnl": vals.get("net", 0.0),
                }
            )
