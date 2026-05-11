import re
from datetime import datetime, time, timedelta
from typing import TypeVar
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Europe/Berlin")
T = TypeVar("T")

_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}|\d{2}\.\d{2}\.\d{4}")


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


def parse_dates(date_str: str) -> list[DateTime]:
    """
    Parse a string of dates and/or date ranges.

    Tokens are separated by commas. Each token is either a single date
    (DD.MM.YYYY or YYYY-MM-DD) or a range of two such dates joined by `-`.
    Examples:
      - "2026-05-11"
      - "11.05.2026,13.05.2026"
      - "2026-05-11-2026-05-15"
      - "11.05.2026,13.05.2026-15.05.2026"
    """
    result: list[DateTime] = []
    seen: set[DateTime] = set()
    for raw in date_str.split(","):
        token = raw.strip()
        if not token:
            continue
        matches = _DATE_RE.findall(token)
        if len(matches) == 1 and token == matches[0]:
            dates = [parse_date(matches[0])]
        elif len(matches) == 2 and token == f"{matches[0]}-{matches[1]}":
            start = parse_date(matches[0])
            end = parse_date(matches[1])
            if start > end:
                raise ValueError(
                    f"Start date {matches[0]} is after end date {matches[1]}"
                )
            span = (end - start).days
            dates = []
            for i in range(span + 1):
                step = start + timedelta(days=i)
                dates.append(DateTime(step.year, step.month, step.day))
        else:
            raise ValueError(f"Invalid date format: {token!r}")
        for d in dates:
            if d not in seen:
                seen.add(d)
                result.append(d)
    if not result:
        raise ValueError(f"No dates parsed from: {date_str!r}")
    return result
