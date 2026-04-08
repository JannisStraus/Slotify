from slotify.wellness.api import get_markdown


def main(days: int) -> str | None:
    return get_markdown(days)
