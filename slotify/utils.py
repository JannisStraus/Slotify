from datetime import datetime, time, timedelta
from typing import TypeVar
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Europe/Berlin")
T = TypeVar("T")


class DateTime(datetime):
    def fmt_en(self) -> str:
        return self.strftime("%Y-%m-%d")

    def __str__(self) -> str:
        return self.strftime("%d.%m.%Y")


class Time(time):
    def __str__(self) -> str:
        return self.strftime("%H:%M")


def choose(title: str, options: dict[str, T]) -> T:
    keys = list(options.keys())

    print(f"\n{title}")
    for i, key in enumerate(keys, start=1):
        print(f"{i:>2}. {key}")

    while True:
        choice = input("Choose number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(keys):
            return options[keys[int(choice) - 1]]
        print("Invalid choice, try again.")


def parse_date(date: str) -> DateTime:
    if "." in date:
        dt = DateTime.strptime(date, "%d.%m.%Y")
    else:
        dt = DateTime.strptime(date, "%Y-%m-%d")
    return dt


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
