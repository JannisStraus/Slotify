import pickle
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from slotify.bot import escape_md2

CACHE_FILE = Path.cwd() / "data" / "cache.pickle"
TZ = ZoneInfo("Europe/Berlin")


def cached_slots(slots: dict[str, list[str]]) -> str | None:
    if not slots:
        return None

    cache = load_cache()

    if cache == slots:
        return None

    save_cache(slots)
    return to_markdown(slots)


def load_cache() -> dict[str, list[str]]:
    if CACHE_FILE.exists():
        data: dict[str, list[str]] = pickle.loads(CACHE_FILE.read_bytes())
        return data
    return {}


def save_cache(slots: dict[str, list[str]]) -> None:
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_bytes(pickle.dumps(slots, protocol=pickle.HIGHEST_PROTOCOL))


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
