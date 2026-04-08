from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from slotify.bot import escape_md2

TZ = ZoneInfo("Europe/Berlin")


def to_markdown(slots: dict[str, list[str]]) -> str:
    header = "*Morante*\n"
    body = "\n".join([f"*{escape_md2(k)}:*\n{', '.join(v)}" for k, v in slots.items()])
    return header + body
