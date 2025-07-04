# data/pipeline.py

from datetime import timedelta
from typing import List, Tuple

from data.importer import load_tradingview_signals, load_tradovate_fills
from data.matching import MatchingEngine, MatchRecord
from data.schemas import TradingViewSignal, TradovateFill


def run_matching_pipeline(
    tradingview_csv: str, tradovate_csv: str, tolerance_min: int = 2
) -> List[MatchRecord]:
    """
    Load signals and fills, normalize & match them.
    Returns a list of MatchRecord(signal, fill).
    """
    signals = list(load_tradingview_signals(tradingview_csv))
    fills = list(load_tradovate_fills(tradovate_csv))

    engine = MatchingEngine(timedelta(minutes=tolerance_min))
    return engine.match(signals, fills)


def run_full_pipeline(
    tradingview_csv: str, tradovate_csv: str, tolerance_min: int = 2
) -> Tuple[List[MatchRecord], List[TradingViewSignal], List[TradovateFill]]:
    """
    Load signals and fills, normalize & match them.
    Returns a tuple of:
      1) matches: List[MatchRecord]
      2) unmatched_signals: List[TradingViewSignal]
      3) unmatched_fills: List[TradovateFill]
    """
    signals = list(load_tradingview_signals(tradingview_csv))
    fills = list(load_tradovate_fills(tradovate_csv))

    engine = MatchingEngine(timedelta(minutes=tolerance_min))
    matches = engine.match(signals, fills)

    # Identify unmatched items
    matched_signals = {m.signal for m in matches}
    matched_fills = {m.fill for m in matches}

    unmatched_signals = [s for s in signals if s not in matched_signals]
    unmatched_fills = [f for f in fills if f not in matched_fills]

    return matches, unmatched_signals, unmatched_fills


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
