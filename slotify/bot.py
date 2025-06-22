import os
import pickle
from pathlib import Path

import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
CACHE_FILE = Path.cwd() / "data" / "cache.pickle"


def send_slots(slots: dict[str, list[str]]) -> None:
    if not slots:
        return

    cache = load_cache()

    if cache == slots:
        return

    save_cache(slots)
    text = to_markdown(slots)
    send_markdown(text)


def to_markdown(slots: dict[str, list[str]]) -> str:
    blocks: list[str] = []
    for d in sorted(slots.keys()):
        header = f"*{d}*"
        times = "\n".join(slots[d])
        blocks.append(f"{header}\n{times}")
    return "\n\n".join(blocks)


def send_markdown(text: str) -> None:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    r = requests.post(url, json=payload, timeout=10)
    r.raise_for_status()


def load_cache() -> dict[str, list[str]]:
    if CACHE_FILE.exists():
        data: dict[str, list[str]] = pickle.loads(CACHE_FILE.read_bytes())
        return data
    return {}


def save_cache(slots: dict[str, list[str]]) -> None:
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_bytes(pickle.dumps(slots, protocol=pickle.HIGHEST_PROTOCOL))
