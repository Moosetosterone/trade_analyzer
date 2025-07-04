from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class Direction(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class TradingViewSignal(BaseModel):
    """Schema for a parsed TradingView alert"""

    model_config = ConfigDict(populate_by_name=True)

    alert_id: int = Field(..., alias="Alert ID")
    raw_ticker: str = Field(..., alias="Ticker")
    name: Optional[str] = Field(None, alias="Name")
    description: str = Field(..., alias="Description")
    timestamp: datetime = Field(..., alias="Time")

    # parsed fields
    symbol: str = Field(..., description="Normalized symbol")
    direction: Direction = Field(..., description="BUY or SELL")
    price: float = Field(..., description="Signal price")
    quantity: int = Field(..., description="Signal quantity")
    order_type: Optional[str] = Field(None, description="Market/Limit etc.")
    sentiment: Optional[str] = Field(None, description="Optional sentiment tag")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Extra fields from payload"
    )


class TradovateFill(BaseModel):
    """Schema for a normalized Tradovate fill record"""

    model_config = ConfigDict(populate_by_name=True)

    order_id: str = Field(..., alias="orderId")
    account: str = Field(..., alias="Account")
    direction: Direction = Field(..., alias="B/S")
    contract: str = Field(..., alias="Contract")
    filled_qty: int = Field(..., alias="filledQty")
    fill_price: float = Field(..., alias="Avg Fill Price")
    timestamp: datetime = Field(..., alias="Fill Time")
    status: str = Field(..., alias="Status")
    order_type: str = Field(..., alias="Type")
    limit_price: Optional[float] = Field(None, alias="Limit Price")
    stop_price: Optional[float] = Field(None, alias="Stop Price")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Extra CSV fields not modeled"
    )
