# models/trade.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import pytz


@dataclass
class TradingViewSignal:
    """Schema for TradingView signal data (SRP)."""

    timestamp: datetime
    symbol: str
    direction: str  # e.g., "long", "flat"
    signal_price: float
    alert_id: Optional[str] = None  # Maps to Alert ID
    strategy_id: Optional[str] = None  # For grouping by strategy (UC3)

    def __post_init__(self):
        """Validate and normalize fields (SRP)."""
        if self.direction not in ["long", "flat"]:
            raise ValueError(f"Invalid direction: {self.direction}")
        if not isinstance(self.timestamp, datetime):
            raise TypeError("Timestamp must be a datetime object")
        if not self.timestamp.tzinfo:
            self.timestamp = self.timestamp.replace(tzinfo=pytz.UTC)
        if self.signal_price < 0:
            raise ValueError("Signal price cannot be negative")


@dataclass
class TradovateFill:
    """Schema for Tradovate execution data (SRP)."""

    timestamp: datetime
    symbol: str
    direction: str  # e.g., "buy", "sell"
    fill_price: float
    qty: int
    order_id: Optional[str] = None  # Unique identifier for matching
    commission: Optional[float] = 0.0  # For P&L calculations (Sprint 3)

    def __post_init__(self):
        """Validate and normalize fields (SRP)."""
        if self.direction not in ["buy", "sell"]:
            raise ValueError(f"Invalid direction: {self.direction}")
        if not isinstance(self.timestamp, datetime):
            raise TypeError("Timestamp must be a datetime object")
        if not self.timestamp.tzinfo:
            self.timestamp = self.timestamp.replace(tzinfo=pytz.UTC)
        if self.fill_price < 0 or self.qty <= 0:
            raise ValueError("Fill price cannot be negative, and qty must be positive")
        if self.commission < 0:
            raise ValueError("Commission cannot be negative")
