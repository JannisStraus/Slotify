import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
TIMEOUT = float(os.getenv("TIMEOUT", "30"))
MD2_SPECIALS = set(r"_*[]()~`>#+-=|{}.!")
MAX_CHARS_SAFE = 3500
