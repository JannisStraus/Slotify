import re

import requests

from slotify.mywellness.parser import SlotInfo, to_markdown
from slotify.utils import DateTime, Time, parse_date


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


def get_slot_infos(date: DateTime, min_minutes: int = 120) -> dict[str, SlotInfo]:
    url = (
        "https://api.sys.mywellness.de/booking/availabilities/startTimes?"
        f"&minMinutes={min_minutes}&dates[]={date.fmt_en()}&outletIds[]=4"
        "&suiteTypeIds[]=4&suiteTypeIds[]=6&suiteTypeIds[]=8&suiteTypeIds[]=2"
        "&suiteTypeIds[]=7&suiteTypeIds[]=1"
    )
    response = requests.get(url, timeout=10.0)
    response.raise_for_status()
    suites = response.json()["result"][0]["outlets"][0]["suiteTypes"]
    # Usually not possible
    if not suites:
        return {}

    slot_infos: dict[str, SlotInfo] = {}
    for suite in suites:
        name = suite["name"]
        times_list: list[tuple[str, str]] = []
        times = suite.get("availableStartTimes", [])
        if not times:
            continue

        parsed_times = sorted(Time.fromisoformat(row["time"]) for row in times)

        start_time = parsed_times[0]
        last_time = parsed_times[0]

        for cur_time in parsed_times[1:]:
            last_minutes = last_time.hour * 60 + last_time.minute
            cur_minutes = cur_time.hour * 60 + cur_time.minute
            if cur_minutes != last_minutes + 10:
                times_list.append((str(start_time), str(last_time)))
                start_time = cur_time
            last_time = cur_time
        times_list.append((str(start_time), str(last_time)))
        slot_infos[name] = {
            "times": times_list,
            "price": suite.get("price"),
        }
    return slot_infos


def get_markdown(date: str) -> str | None:
    # non_defaults: list[tuple[str, str]] = []

    # slug = os.getenv("WELLNEST_SLUG")
    # if not slug:
    #     slugs = get_slugs()
    #     slug = choose("Choose location", slugs)
    #     non_defaults.append(("WELLNEST_SLUG", slug))
    #     os.environ["WELLNEST_SLUG"] = slug

    # if non_defaults:
    #     print(
    #         "Tip: To reuse the same location, add the following "
    #         "environment variable to your '.env' file:"
    #     )
    #     for key, value in non_defaults:
    #         print(f'{key}="{value}"')

    date_time = parse_date(date)
    slots = get_slot_infos(date_time)
    if not slots:
        return None
    return to_markdown(str(date_time), slots)
