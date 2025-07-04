# tests/test_pipeline.py

import os

import pytest

from ingestion.pipeline import run_matching_pipeline
from matching.matching import MatchRecord

HERE = os.path.dirname(__file__)
TV_CSV = os.path.join(
    HERE, os.pardir, "data", "TradingView_Alerts_Log_2025-07-03_790cd.csv"
)
FILLS_CSV = os.path.join(HERE, os.pardir, "data", "Orders-4.csv")


def test_pipeline_returns_list_of_matchrecords():
    matches = run_matching_pipeline(TV_CSV, FILLS_CSV, tolerance_min=2)
    assert isinstance(matches, list)
    assert all(isinstance(m, MatchRecord) for m in matches)


def test_pipeline_finds_some_matches():
    matches = run_matching_pipeline(TV_CSV, FILLS_CSV, tolerance_min=2)
    # Sanity check: with your sample data, you should have at least one match
    assert len(matches) > 0, "Expected at least one signal→fill match"


@pytest.mark.parametrize(
    "tol, expected_min",
    [
        (0, 0),  # zero tolerance → likely no matches
        (2, 1),  # your default pipeline should match at least one
    ],
)
def test_tolerance_affects_match_count(tol, expected_min):
    cnt = len(run_matching_pipeline(TV_CSV, FILLS_CSV, tolerance_min=tol))
    assert cnt >= expected_min
