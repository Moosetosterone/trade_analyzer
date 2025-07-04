from datetime import date
from typing import Any, Callable, Dict, List, Optional, TypeVar

T = TypeVar("T")


def group_by(records: List[T], key_func: Callable[[T], Any]) -> Dict[Any, List[T]]:
    """
    Generic grouping: returns a dict mapping key to list of records.
    """
    groups: Dict[Any, List[T]] = {}
    for r in records:
        key = key_func(r)
        groups.setdefault(key, []).append(r)
    return groups


def group_by_instrument(records: List[T]) -> Dict[str, List[T]]:
    """
    Group records by their 'symbol' attribute.
    """
    return group_by(records, lambda r: getattr(r, "symbol", None))


def group_by_date(records: List[T]) -> Dict[date, List[T]]:
    """
    Group records by their 'date' attribute.
    """
    return group_by(records, lambda r: getattr(r, "date", None))


def filter_by_date_range(
    records: List[T], start_date: Optional[date] = None, end_date: Optional[date] = None
) -> List[T]:
    """
    Filter records whose 'date' attribute falls within [start_date, end_date].
    """
    filtered: List[T] = []
    for r in records:
        d = getattr(r, "date", None)
        if d is None:
            continue
        if start_date and d < start_date:
            continue
        if end_date and d > end_date:
            continue
        filtered.append(r)
    return filtered
