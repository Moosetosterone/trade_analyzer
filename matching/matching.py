# data/matching.py

from datetime import timedelta
from typing import List, Tuple

from models.schemas import TradingViewSignal, TradovateFill


class MatchRecord:
    """
    A simple container tying one TradingViewSignal to one TradovateFill.
    """

    def __init__(self, signal: TradingViewSignal, fill: TradovateFill):
        self.signal = signal
        self.fill = fill


class MatchingEngine:
    """
    Matches signals to fills by symbol, direction, and a time‐tolerance window.
    """

    def __init__(self, tolerance: timedelta = timedelta(minutes=2)):
        self.tolerance = tolerance

    def match(
        self, signals: List[TradingViewSignal], fills: List[TradovateFill]
    ) -> List[MatchRecord]:
        matches: List[MatchRecord] = []
        unused_fills = fills.copy()

        for sig in signals:
            # sort fills by timestamp so we match earliest fill first
            for fill in sorted(unused_fills, key=lambda f: f.timestamp):
                # same contract and same side?
                if fill.contract == sig.symbol and fill.direction == sig.direction:
                    # within tolerance?
                    delta = abs(fill.timestamp - sig.timestamp)
                    if delta <= self.tolerance:
                        matches.append(MatchRecord(sig, fill))
                        unused_fills.remove(fill)
                        break  # move on to next signal
        return matches
