from typing import TypedDict

from slotify.bot import escape_md2


class SlotInfo(TypedDict):
    times: list[tuple[str, str]]
    price: int


def to_markdown(date: str, slots: dict[str, SlotInfo]) -> str:
    header = f"*MyWellness {escape_md2(date)}*\n"
    body = "\n".join(
        [
            f"*{k} \\({v['price']}€\\):*\n{', '.join([f'{s}\\-{e}' for s, e in v['times']])}"
            for k, v in slots.items()
        ]
    )
    return header + body
