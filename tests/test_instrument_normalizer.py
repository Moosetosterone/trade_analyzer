# tests/test_instrument_normalizer.py

from datetime import datetime

import pytest

from normalization.instrument_normalizer import InstrumentNormalizer


@pytest.fixture
def norm():
    # Assumes your YAML lives at this path in the repo root
    return InstrumentNormalizer("config/instrument_mapping.yaml")


def test_generic_cleanup(norm):
    # Strips exchange prefix and timeframe suffix
    raw = "CME:MGCQ2025, 3m"
    assert norm.normalize(raw, datetime(2025, 7, 3)) == "MGCQ2025"


def test_wildcard_rollover(norm):
    # With rollover_day=1, every day >=1 rolls to the next month
    # June 15 → month 6 → rollover → month 7 (code N) → "MESN25"
    raw = "MES1!"
    dt = datetime(2025, 6, 15)
    assert norm.normalize(raw, dt) == "MESN25"


def test_end_of_year_rollover(norm):
    # December 10 → month 12 → rollover → month 1 of next year → "MESF26"
    raw = "MES1!"
    dt = datetime(2025, 12, 10)
    assert norm.normalize(raw, dt) == "MESF26"
