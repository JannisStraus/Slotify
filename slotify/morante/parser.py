from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from slotify.bot import escape_md2

CACHE_FILE = Path.cwd() / "data" / "cache.json"
TZ = ZoneInfo("Europe/Berlin")


def to_markdown(slots: dict[str, list[str]]) -> str:
    header = "*Morante*\n"
    body = "\n".join([f"*{escape_md2(k)}:*\n{', '.join(v)}" for k, v in slots.items()])
    return header + body


def days_to_datetime(days: int) -> tuple[str, str]:
    now = datetime.now(TZ)
    start_time = now.isoformat(timespec="seconds")
    end_date = (now + timedelta(days=days)).date()
    end_dt = datetime(
        end_date.year,
        end_date.month,
        end_date.day,
        23,
        59,
        59,
        tzinfo=TZ,
    )
    end_time = end_dt.isoformat(timespec="seconds")
    return start_time, end_time


def utc_to_local(ts: str) -> tuple[str, str]:
    dt_local = datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(TZ)
    return dt_local.strftime("%d.%m.%y"), dt_local.strftime("%H:%M")
