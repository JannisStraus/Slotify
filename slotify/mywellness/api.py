import requests
import os
import re
import datetime
from slotify.utils import choose

from slotify.wellnest.parser import parse_date, to_markdown

def get_slugs() -> dict[str, str]:
    url = (
        "https://wellnest.me/wp-content/plugins/"
        "booking-tool-vue/app/js/app.js?ver=1774615677"
    )
    js = requests.get(url, timeout=10.0).text
    pattern = r'name:\s*"([^"]+)"[^}]*?slug:\s*"([^"]+)"'
    matches = re.findall(pattern, js)
    slug_to_name = dict(matches)
    return slug_to_name


# def slot_available(date_from: str, date_to: str) -> set[str]:
#     url = (
#         f"https://wmi.wellnest.me/api/v1/slot-ranges/ess1?date_start={date_from}"
#         f"&date_end={date_to}&disability_friendly_nest_required=false"
#     )
#     response = requests.get(url, timeout=10.0)
#     response.raise_for_status()
#     msg = response.json()["message"]
#     return {str(msg[d]) for d in msg if d == ">=1"}


def get_slot_times(date: str, min_minutes: int = 120) -> dict[str, tuple[str, str]]:
    url = (
        "https://api.sys.mywellness.de/booking/availabilities/startTimes?"
        f"&minMinutes={min_minutes}&dates[]={date}&outletIds[]=4&suiteTypeIds[]=4"
        "&suiteTypeIds[]=6&suiteTypeIds[]=8&suiteTypeIds[]=2&suiteTypeIds[]=7&"
        "suiteTypeIds[]=1"
    )
    response = requests.get(url, timeout=10.0)
    response.raise_for_status()
    suites = response.json()["result"][0]["suiteTypes"]
    # Usually not possible
    if not suites:
        return {}
    
    slots: dict[str, tuple[str, str]] = {}
    for suite in suites:
        name = suite["name"]
        price = suite["price"]
        times = suite["availableStartTimes"]
        last_time = datetime.time()
        start_time = datetime.time()
        end_time = datetime.time()
        for row in times:
            hour, minute = row["time"].split(":")
            cur_time = datetime.time(int(hour), int(minute))
            if not last_time:
                last_time = cur_time
                start_time = cur_time
                continue
            if cur_time != last_time + datetime.timedelta(minutes=10):
                end_time = cur_time
                slots[]



def get_markdown(date: str) -> str | None:
    non_defaults: list[tuple[str, str]] = []

    slug = os.getenv("WELLNEST_SLUG")
    if not slug:
        slugs = get_slugs()
        slug = choose("Choose location", slugs)
        non_defaults.append(("WELLNEST_SLUG", slug))
        os.environ["WELLNEST_SLUG"] = slug

    if non_defaults:
        print(
            "Tip: To reuse the same location, add the following "
            "environment variable to your '.env' file:"
        )
        for key, value in non_defaults:
            print(f'{key}="{value}"')

    date_en, date_de = parse_date(date)
    slots = get_slot_times(date_en, slug)
    if not slots:
        return None
    return to_markdown(date_de, slots)
