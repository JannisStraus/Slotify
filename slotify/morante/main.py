from slotify.morante.api import get_markdown


def main(days: int) -> str | None:
    return get_markdown(days)
