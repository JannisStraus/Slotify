from slotify.morante.api import get_businesses


def main(next_days: int) -> str | None:
    # html = search_slot()
    # slots = parse_agenda(html, next_days)
    # return get_slots(slots)
    return str(get_businesses())
