from slotify.morante.api import get_markdown


def main(date: str) -> str | None:
    return get_markdown(date)
