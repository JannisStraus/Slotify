import re

import requests

from slotify.justiz.parser import to_markdown
from slotify.utils import parse_date, DateTime


def get_times(date: DateTime) -> list[dict[str, str]]:
    url = (
        "https://www.justiztermine.nrw.de/api/public/de/available_times"
        f"?participants_count=1&agency_id=59&service_id=12&date_choice={date.fmt_en()}"
    )
    response = requests.get(url)
    data = response.json()["data"]
    if not data:
        return []
    return data[0]["times"]


def get_markdown(date: str) -> str | None:
    date_time = parse_date(date)
    dates = get_times(date_time)
    if not dates:
        return None
    return to_markdown(str(date_time), dates)
