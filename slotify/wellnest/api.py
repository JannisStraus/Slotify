import requests

from slotify.wellnest.parser import parse_date, to_markdown

# def slot_available(date: str) -> bool:
#     url = (
#         "https://wmi.wellnest.me/api/v1/slot-ranges/ess1?"
#         f"date_start={date}&date_end={date}&disability_friendly_nest_required=false"
#     )
#     response = requests.get(url)
#     response.raise_for_status()
#     msg = response.json()["message"]
#     return str(msg[date]) == ">=1"


def get_slots(date: str) -> dict[str, list[str]] | None:
    url = (
        "https://wmi.wellnest.me/api/v1/day-slots/ess1?"
        f"date={date}&disability_friendly_nest_required=false"
    )
    response = requests.get(url)
    response.raise_for_status()
    msg = response.json()["message"]
    if not msg:
        return None
    return {k: list(v.keys()) for k, v in msg.items()}


def get_markdown(date: str) -> str | None:
    date_en, date_de = parse_date(date)
    slots = get_slots(date_en)
    if not slots:
        return None
    return to_markdown(date_de, slots)
