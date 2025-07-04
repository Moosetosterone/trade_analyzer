# data/importer.py

import csv
from typing import Dict, Iterator

from data.instrument_normalizer import InstrumentNormalizer
from data.normalizer import TradingViewSignalFactory, TradovateFillFactory
from data.schemas import TradingViewSignal, TradovateFill

# load once at module import
_instrument_norm = InstrumentNormalizer("config/instrument_mapping.yaml")


def load_tradingview_signals(csv_path: str) -> Iterator[TradingViewSignal]:
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sig: TradingViewSignal = TradingViewSignalFactory.from_csv_row(row)
            canonical = _instrument_norm.normalize(sig.symbol, sig.timestamp)
            # override the parsed symbol
            sig = sig.model_copy(update={"symbol": canonical})
            yield sig


def load_tradovate_fills(csv_path: str) -> Iterator[TradovateFill]:
    """
    Reads the Tradovate fills CSV and yields UTC-normalized TradovateFill objects
    with `contract` replaced by the canonical symbol.
    """
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            fill: TradovateFill = TradovateFillFactory.from_csv_row(row)
            # compute canonical symbol
            canonical = _instrument_norm.normalize(fill.contract, fill.timestamp)
            # override the contract field
            fill = fill.model_copy(update={"contract": canonical})
            yield fill
