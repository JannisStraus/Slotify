import argparse
from dataclasses import dataclass
from importlib import import_module
from typing import Any

from slotify.loop import run_loop


@dataclass(frozen=True)
class BotConfig:
    help: str
    flag_short: str
    flag_long: str
    flag_kwargs: dict[str, Any]
    module: str
    param: str


BOTS: dict[str, BotConfig] = {
    "morante": BotConfig(
        help="Morante Hair Salon bot",
        flag_short="-d",
        flag_long="--days",
        flag_kwargs={
            "type": int,
            "required": True,
            "help": "Number of days in advance for which to search for available slots.",
        },
        module="slotify.morante.main",
        param="days",
    ),
    "wellnest": BotConfig(
        help="Wellnest bot",
        flag_short="-d",
        flag_long="--date",
        flag_kwargs={
            "type": str,
            "required": True,
            "help": "Date (DD.MM.YYYY or YYYY-MM-DD) to search for available slots.",
        },
        module="slotify.wellnest.main",
        param="date",
    ),
    "mywellness": BotConfig(
        help="MyWellness bot",
        flag_short="-d",
        flag_long="--date",
        flag_kwargs={
            "type": str,
            "required": True,
            "help": "Date (DD.MM.YYYY or YYYY-MM-DD) to search for available slots.",
        },
        module="slotify.mywellness.main",
        param="date",
    ),
    "justiz": BotConfig(
        help="Justiz bot",
        flag_short="-d",
        flag_long="--date",
        flag_kwargs={
            "type": str,
            "required": True,
            "help": "Date (DD.MM.YYYY or YYYY-MM-DD) to search for available slots.",
        },
        module="slotify.justiz.main",
        param="date",
    ),
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Slotify: Search for available slots.")
    subparsers = parser.add_subparsers(dest="bot", required=True, help="Bot to run")

    for name, cfg in BOTS.items():
        sub = subparsers.add_parser(name, help=cfg.help)
        sub.add_argument(
            "-m",
            "--minutes",
            type=int,
            default=5,
            help="Number of minutes to wait between checks (default: 5).",
        )
        sub.add_argument(cfg.flag_short, cfg.flag_long, **cfg.flag_kwargs)

    args = parser.parse_args()
    cfg = BOTS[args.bot]
    bot_main = import_module(cfg.module).main
    run_loop(args.minutes, bot_main, getattr(args, cfg.param))


if __name__ == "__main__":
    main()
