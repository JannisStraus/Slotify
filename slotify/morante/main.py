from slotify.morante.parser import get_slots, parse_agenda
from slotify.morante.webscraper import search_slot


def main(next_days: int) -> str | None:
    html = search_slot()
    slots = parse_agenda(html, next_days)
    return get_slots(slots)
