import os
import re

import requests

from slotify.config import TIMEOUT
from slotify.utils import DateTime, choose
from slotify.wellnest.parser import to_markdown


def get_slugs() -> dict[str, str]:
    url = (
        "https://wellnest.me/wp-content/plugins/"
        "booking-tool-vue/app/js/app.js?ver=1774615677"
    )
    js = requests.get(url, timeout=TIMEOUT).text
    pattern = r'name:\s*"([^"]+)"[^}]*?slug:\s*"([^"]+)"'
    matches = re.findall(pattern, js)
    slug_to_name = dict(matches)
    return slug_to_name


# def slot_available(date_from: str, date_to: str) -> set[str]:
#     url = (
#         f"https://wmi.wellnest.me/api/v1/slot-ranges/ess1?date_start={date_from}"
#         f"&date_end={date_to}&disability_friendly_nest_required=false"
#     )
#     response = requests.get(url, timeout=TIMEOUT)
#     response.raise_for_status()
#     msg = response.json()["message"]
#     return {str(msg[d]) for d in msg if d == ">=1"}


def get_slot_times(date: DateTime, slug: str) -> dict[str, list[str]]:
    url = (
        f"https://wmi.wellnest.me/api/v1/day-slots/{slug}?"
        f"date={date.fmt_en()}&disability_friendly_nest_required=false"
    )
    response = requests.get(url, timeout=TIMEOUT)
    response.raise_for_status()
    msg = response.json()["message"]
    if not msg:
        return {}
    return {k: list(v.keys()) for k, v in msg.items()}


def get_markdown(date: DateTime) -> str | None:
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

    slots = get_slot_times(date, slug)
    if not slots:
        return None
    return to_markdown(str(date), slots)
