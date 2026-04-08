from typing import Any
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from slotify.bot import escape_md2

TZ = ZoneInfo("Europe/Berlin")

def choose(title: str, options: dict[str, Any]) -> Any:
    keys = list(options.keys())

    print(f"\n{title}")
    for i, key in enumerate(keys, start=1):
        print(f"{i:>2}. {key}")

    while True:
        choice = input("Choose number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(keys):
            return options[keys[int(choice) - 1]]
        print("Invalid choice, try again.")


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
