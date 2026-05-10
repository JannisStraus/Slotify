from slotify.bot import escape_md2


def to_markdown(date: str, times: list[dict[str, str]]) -> str:
    header = f"*Justiz {escape_md2(date)}*\n"
    body = ", ".join([time["time"] for time in times])
    return header + body
