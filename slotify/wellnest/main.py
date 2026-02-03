from slotify.wellnest.api import slot_available
from slotify.wellnest.parser import parse_date


def main(date: str) -> str | None:
    date = parse_date(date)
    if slot_available(date):
        return f"Slot available at Wellnest on {date}!"
    return None
