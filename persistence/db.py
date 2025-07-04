# FILE: data/db.py
from datetime import datetime
from typing import Optional

from sqlalchemy import JSON, Column
from sqlmodel import Field, Session, SQLModel, create_engine, select


# --------------------------------------
# Database Models
# --------------------------------------
class Instrument(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(index=True, unique=True)


class Signal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    instrument_id: int = Field(foreign_key="instrument.id", index=True)
    timestamp: datetime
    direction: str
    price: float
    quantity: int
    extra: dict = Field(sa_column=Column("metadata", JSON))


class Fill(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    instrument_id: int = Field(foreign_key="instrument.id", index=True)
    timestamp: datetime
    direction: str
    price: float
    quantity: int
    extra: dict = Field(sa_column=Column("metadata", JSON))


# --------------------------------------
# Helper Functions
# --------------------------------------


def init_db(db_url: str = "sqlite:///data/trades.db"):
    """
    Create the SQLite database (if not exists) and return the engine.
    """
    engine = create_engine(db_url, echo=False)
    SQLModel.metadata.create_all(engine)
    return engine


def get_session(engine):
    """Return a new Session object for the given engine."""
    return Session(engine)


def upsert_instrument(session: Session, symbol: str) -> Instrument:
    stmt = select(Instrument).where(Instrument.symbol == symbol)
    inst = session.exec(stmt).first()
    if not inst:
        inst = Instrument(symbol=symbol)
        session.add(inst)
        session.commit()
        session.refresh(inst)
    return inst


def insert_signal(session: Session, signal) -> Signal:
    inst = upsert_instrument(session, signal.symbol)
    rec = Signal(
        instrument_id=inst.id,
        timestamp=signal.timestamp,
        direction=(
            signal.direction.value
            if hasattr(signal.direction, "value")
            else signal.direction
        ),
        price=signal.price,
        quantity=signal.quantity,
        extra=signal.metadata,
    )
    session.add(rec)
    session.commit()
    session.refresh(rec)
    return rec


def insert_fill(session: Session, fill) -> Fill:
    inst = upsert_instrument(session, fill.contract)
    rec = Fill(
        instrument_id=inst.id,
        timestamp=fill.timestamp,
        direction=(
            fill.direction.value if hasattr(fill.direction, "value") else fill.direction
        ),
        price=fill.fill_price,
        quantity=fill.filled_qty,
        extra=fill.metadata,
    )
    session.add(rec)
    session.commit()
    session.refresh(rec)
    return rec
