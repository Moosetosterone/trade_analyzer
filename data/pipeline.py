# data/pipeline.py

from datetime import timedelta
from typing import List

from data.importer import load_tradingview_signals, load_tradovate_fills
from data.matching import MatchingEngine, MatchRecord


def run_matching_pipeline(
    tradingview_csv: str, tradovate_csv: str, tolerance_min: int = 2
) -> List[MatchRecord]:
    """
    Load signals and fills from CSV, normalize & match them.

    :param tradingview_csv: path to your TradingView alerts CSV
    :param tradovate_csv:   path to your Tradovate fills CSV
    :param tolerance_min:   matching window, in minutes
    :return:                list of MatchRecord(signal, fill)
    """
    signals = list(load_tradingview_signals(tradingview_csv))
    fills = list(load_tradovate_fills(tradovate_csv))

    engine = MatchingEngine(tolerance=timedelta(minutes=tolerance_min))
    return engine.match(signals, fills)


if __name__ == "__main__":
    import sys

    tv_csv = sys.argv[1]
    tv2_csv = sys.argv[2]
    recs = run_matching_pipeline(tv_csv, tv2_csv)
    print(f"Found {len(recs)} matches:")
    for r in recs:
        print(
            f"  {r.signal.symbol} @ {r.signal.timestamp} → {r.fill.fill_price} @ {r.fill.timestamp}"
        )
