from datetime import datetime

from slotify.bot import escape_md2


def to_markdown(date: str, slots: dict[str, list[str]]) -> str:
    header = f"*Wellnest {escape_md2(date)}*\n"
    body = "\n".join([f"*{k} min:*\n{', '.join(v)}" for k, v in slots.items()])
    return header + body


def parse_date(date: str) -> tuple[str, str]:
    if "." in date:
        dt = datetime.strptime(date, "%d.%m.%Y")
    else:
        dt = datetime.strptime(date, "%Y-%m-%d")
    return dt.strftime("%Y-%m-%d"), dt.strftime("%d.%m.%Y")
