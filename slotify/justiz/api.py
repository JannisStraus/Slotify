import requests

from slotify.justiz.parser import to_markdown
from slotify.utils import DateTime


def get_times(date: DateTime) -> list[dict[str, str]]:
    url = (
        "https://www.justiztermine.nrw.de/api/public/de/available_times"
        f"?participants_count=1&agency_id=59&service_id=12&date_choice={date.fmt_en()}"
    )
    response = requests.get(url)
    data = response.json()["data"]
    if not data:
        return []
    times: list[dict[str, str]] = data[0]["times"]
    return times


def get_markdown(date: DateTime) -> str | None:
    times = get_times(date)
    if not times:
        return None
    return to_markdown(str(date), times)
