import requests


def slot_available(date: str) -> bool:
    url = (
        "https://wmi.wellnest.me/api/v1/slot-ranges/ess1?"
        f"date_start={date}&date_end={date}&disability_friendly_nest_required=false"
    )
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    slot = data["message"][date]
    if not isinstance(slot, str):
        raise ValueError(
            f"Expected slot to be str for date '{date}', "
            f"got {type(slot).__name__}: {slot!r}"
        )
    return slot == ">=1"
