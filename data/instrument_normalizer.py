import re
from datetime import datetime
from typing import Any, Dict

import yaml


class InstrumentNormalizer:
    """
    Normalizes raw tickers into a canonical contract symbol.
    """

    def __init__(self, mapping_path: str):
        # Load configuration
        with open(mapping_path) as f:
            cfg = yaml.safe_load(f)
        self.month_codes: Dict[str, int] = cfg.get("month_codes", {})
        self.overrides: Dict[str, str] = cfg.get("overrides", {})
        self.rollover_day: int = cfg.get("rollover_day", 1)
        # Reverse lookup for month_code -> letter
        self.code_for_month = {v: k for k, v in self.month_codes.items()}

    def normalize(self, raw: str, trade_date: datetime) -> str:
        # 1) Check for explicit overrides
        if raw in self.overrides:
            return self.overrides[raw]

        # 2) Handle wildcard contracts ending in '1!'
        if raw.endswith("1!"):
            root = raw[:-2]
            month = trade_date.month
            year = trade_date.year
            # roll to next month if on/after rollover_day
            if trade_date.day >= self.rollover_day:
                month += 1
                if month > 12:
                    month = 1
                    year += 1
            code = self.code_for_month.get(month)
            return f"{root}{code}{str(year)[-2:]}"

        # 3) Strip exchange prefixes and timeframe suffixes
        s = re.sub(r"^[A-Z]+:", "", raw)
        s = re.sub(r",\s*\d+[mMhHdDwW]$", "", s)

        # 4) Normalize contracts with embedded year digits (e.g. 'MESU5', 'MGCQ2025')
        m = re.match(r"^([A-Z]+)([FGHJKMNQUVXZ])(\d+)$", s)
        if m:
            root, code_letter, year_digits = m.groups()
            # Compute full year based on length of year_digits and current trade_date
            base = (trade_date.year // (10 ** len(year_digits))) * (
                10 ** len(year_digits)
            )
            year_full = base + int(year_digits)
            return f"{root}{code_letter}{year_full}"

        # 5) Fallback: return cleaned string
        return s
