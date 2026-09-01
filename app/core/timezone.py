from datetime import datetime, timezone
from zoneinfo import ZoneInfo

BRAZIL_TZ = ZoneInfo("America/Recife")
UTC = timezone.utc

def to_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        value = value.replace(tzinfo=BRAZIL_TZ)
    return value.astimezone(UTC)

def month_bounds_utc(year: int, month: int) -> tuple[datetime, datetime]:
    start = datetime(year, month, 1, tzinfo=BRAZIL_TZ)
    nxt = datetime(year + 1, 1, 1, tzinfo=BRAZIL_TZ) if month == 12 else datetime(year, month + 1, 1, tzinfo=BRAZIL_TZ)
    return start.astimezone(UTC), nxt.astimezone(UTC)
