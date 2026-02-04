import os

import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
_MD2_SPECIALS = set(r"_*[]()~`>#+-=|{}.!")


def redact(s: str) -> str:
    return s.replace(BOT_TOKEN, "[BOT_TOKEN]").replace(CHAT_ID, "[CHAT_ID]")


def escape_md2(text: str) -> str:
    out = []
    for ch in text:
        if ch in _MD2_SPECIALS:
            out.append(f"\\{ch}")
        else:
            out.append(ch)
    return "".join(out)


def send_markdown(text: str, error: bool = False) -> None:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    if error:
        text = escape_md2(redact(text))
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "MarkdownV2"}

    r = requests.post(url, json=payload)
    if r.status_code == 400:
        payload["text"] = (
            "HTTPError: 400 Client Error\n"
            f"URL: {escape_md2(redact(url))}\n```Message:\n{escape_md2(text)}```"
        )
        r = requests.post(url, json=payload)
    r.raise_for_status()
