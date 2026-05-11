from slotify.utils import parse_dates
from slotify.wellnest.api import get_markdown


def main(date: str) -> str | None:
    parts = [md for d in parse_dates(date) if (md := get_markdown(d))]
    return "\n\n".join(parts) if parts else None
