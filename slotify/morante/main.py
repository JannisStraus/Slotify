from slotify.morante.api import slot_available


def main(days: int) -> str | None:
    return slot_available(days)
