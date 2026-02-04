from slotify.wellnest.api import get_markdown


def main(date: str) -> str | None:
    return get_markdown(date)
