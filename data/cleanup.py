# data/cleanup.py
import logging
from datetime import datetime
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)


class DataCleaner:
    """Cleans and normalizes Tradovate CSV data (SRP)."""

    @staticmethod
    def clean_cash_history(
        cash_df: pd.DataFrame, is_test: bool = False
    ) -> pd.DataFrame:
        """Cleans Cash History.csv by normalizing timestamps and fee types."""
        if cash_df is None or cash_df.empty:
            logger.debug("No cash history data provided or empty")
            return cash_df

        # Create a copy to avoid modifying the input
        cleaned_df = cash_df.copy()

        # Normalize Cash Change Type
        if "Cash Change Type" in cleaned_df.columns:
            cleaned_df["Cash Change Type"] = (
                cleaned_df["Cash Change Type"].str.strip().str.lower()
            )
            logger.debug(
                f"Normalized Cash Change Types: {cleaned_df['Cash Change Type'].unique()}"
            )

        # Filter out NaN contracts
        cleaned_df = cleaned_df[cleaned_df["Contract"].notna()]

        # Normalize timestamps
        if "Timestamp" in cleaned_df.columns:
            for fmt in ["%m/%d/%Y %H:%M:%S.%f", "%m/%d/%Y %H:%M:%S"]:
                cleaned_df["Timestamp"] = pd.to_datetime(
                    cleaned_df["Timestamp"], format=fmt, errors="coerce"
                )
                if cleaned_df["Timestamp"].notna().any():
                    break
            cleaned_df = cleaned_df[cleaned_df["Timestamp"].notna()]
            if is_test:
                cleaned_df["Timestamp"] = cleaned_df["Timestamp"].dt.tz_localize("UTC")
                logger.debug("Assumed cash_df Timestamps in UTC for test")
            else:
                if not cleaned_df["Timestamp"].dt.tz:
                    cleaned_df["Timestamp"] = (
                        cleaned_df["Timestamp"]
                        .dt.tz_localize("America/New_York")
                        .dt.tz_convert("UTC")
                    )
                    logger.debug("Converted cash_df Timestamps from EDT to UTC")

        return cleaned_df

    @staticmethod
    def clean_fill_data(fill_df: pd.DataFrame, is_test: bool = False) -> pd.DataFrame:
        """Cleans Orders-4.csv by normalizing timestamps and directions."""
        if fill_df is None or fill_df.empty:
            logger.debug("No fill data provided or empty")
            return fill_df

        # Create a copy to avoid modifying the input
        cleaned_df = fill_df.copy()

        # Normalize B/S
        if "B/S" in cleaned_df.columns:
            cleaned_df["B/S"] = cleaned_df["B/S"].str.strip().str.lower()
            logger.debug(f"Normalized B/S values: {cleaned_df['B/S'].unique()}")

        # Normalize timestamps
        if "Fill Time" in cleaned_df.columns:
            for fmt in ["%m/%d/%Y %H:%M:%S.%f", "%m/%d/%Y %H:%M:%S"]:
                cleaned_df["Fill Time"] = pd.to_datetime(
                    cleaned_df["Fill Time"], format=fmt, errors="coerce"
                )
                if cleaned_df["Fill Time"].notna().any():
                    break
            cleaned_df = cleaned_df[cleaned_df["Fill Time"].notna()]
            if is_test:
                cleaned_df["Fill Time"] = cleaned_df["Fill Time"].dt.tz_localize("UTC")
                logger.debug("Assumed fill_df Fill Time in UTC for test")
            else:
                if not cleaned_df["Fill Time"].dt.tz:
                    cleaned_df["Fill Time"] = (
                        cleaned_df["Fill Time"]
                        .dt.tz_localize("America/New_York")
                        .dt.tz_convert("UTC")
                    )
                    logger.debug("Converted fill_df Fill Time from EDT to UTC")

        return cleaned_df
