# data/normalizer.py

import json
from datetime import datetime
from typing import Dict, Optional
from zoneinfo import ZoneInfo

from data.schemas import Direction, TradingViewSignal, TradovateFill


class TradingViewSignalFactory:
    """Parse a raw CSV row into a fully-populated TradingViewSignal."""

    UTC = ZoneInfo("UTC")

    @staticmethod
    def from_csv_row(row: Dict[str, str]) -> TradingViewSignal:
        # ─── Updated timestamp parsing ───────────────────────────────────────
        ts_raw = row["Time"]
        try:
            # e.g. "2025-07-03T14:28:01Z"
            if ts_raw.endswith("Z"):
                ts = datetime.fromisoformat(ts_raw.replace("Z", "+00:00"))
            else:
                ts = datetime.fromisoformat(ts_raw)
        except ValueError:
            # fall back to legacy format
            ts = datetime.strptime(ts_raw, "%Y-%m-%d %H:%M:%S")
            ts = ts.replace(tzinfo=TradingViewSignalFactory.UTC)
        # ensure it's UTC-aware
        ts = ts.astimezone(TradingViewSignalFactory.UTC)
        row["Time"] = ts.isoformat()
        # ─────────────────────────────────────────────────────────────────────

        # 2) Parse the JSON payload in 'Description'
        payload = json.loads(row["Description"])
        row["symbol"] = payload["ticker"]
        row["direction"] = payload["action"].upper()
        row["price"] = float(payload["price"])
        row["quantity"] = int(payload["quantity"])
        row["order_type"] = payload.get("orderType")
        row["sentiment"] = payload.get("sentiment")
        row["metadata"] = {
            k: v
            for k, v in payload.items()
            if k
            not in {
                "ticker",
                "action",
                "price",
                "quantity",
                "orderType",
                "sentiment",
                "time",
            }
        }

        # 3) Delegate to Pydantic for validation/coercion
        return TradingViewSignal.model_validate(row)


class TradovateFillFactory:
    """Parse a raw CSV row (dict of strings) into a UTC-normalized TradovateFill."""

    LOCAL_TZ = ZoneInfo("America/New_York")

    @staticmethod
    def from_csv_row(row: Dict[str, str]) -> TradovateFill:
        # 1) Parse & normalize the Fill Time:
        ts_raw = row["Fill Time"]
        # try ISO8601 (with Z or offset)
        try:
            if ts_raw.endswith("Z"):
                dt = datetime.fromisoformat(ts_raw.replace("Z", "+00:00"))
            else:
                dt = datetime.fromisoformat(ts_raw)
        except ValueError:
            # fallback #1: YYYY-MM-DD HH:MM:SS
            try:
                dt = datetime.strptime(ts_raw, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                # fallback #2: MM/DD/YYYY HH:MM:SS
                dt = datetime.strptime(ts_raw, "%m/%d/%Y %H:%M:%S")
        # localize & convert to UTC
        local_ts = dt.replace(tzinfo=TradovateFillFactory.LOCAL_TZ)
        utc_ts = local_ts.astimezone(ZoneInfo("UTC"))
        row["Fill Time"] = utc_ts.isoformat()
        # stash original
        row["metadata"] = {"local_timestamp": local_ts.isoformat()}

        # 1b) Normalize the B/S field
        row["B/S"] = row.get("B/S", "").strip().upper()

        # 2) Clean up empty-strings for optional floats:
        for key in ("Limit Price", "Stop Price"):
            val = row.get(key, "").strip()
            row[key] = float(val) if val else None

        # 3) Delegate to Pydantic for the rest:
        return TradovateFill.model_validate(row)
