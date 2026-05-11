import argparse
from dataclasses import dataclass
from importlib import import_module

from slotify.loop import run_loop


@dataclass(frozen=True)
class BotConfig:
    help: str
    module: str


BOTS: dict[str, BotConfig] = {
    "morante": BotConfig(
        help="Morante Hair Salon bot",
        module="slotify.morante.main",
    ),
    "wellnest": BotConfig(
        help="Wellnest bot",
        module="slotify.wellnest.main",
    ),
    "mywellness": BotConfig(
        help="MyWellness bot",
        module="slotify.mywellness.main",
    ),
    "justiz": BotConfig(
        help="Justiz bot",
        module="slotify.justiz.main",
    ),
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Slotify: Search for available slots.")
    subparsers = parser.add_subparsers(dest="bot", required=True, help="Bot to run")

    date_help = (
        "Date(s) to search for available slots. Accepts single dates "
        "(DD.MM.YYYY or YYYY-MM-DD), comma-separated lists, ranges "
        "joined by '-', or a combination. "
        "Example: '2026-05-11,2026-05-13-2026-05-15'."
    )

    for name, cfg in BOTS.items():
        sub = subparsers.add_parser(name, help=cfg.help)
        sub.add_argument(
            "-m",
            "--minutes",
            type=int,
            default=5,
            help="Number of minutes to wait between checks (default: 5).",
        )
        sub.add_argument(
            "-d",
            "--date",
            type=str,
            required=True,
            help=date_help,
        )

    args = parser.parse_args()
    cfg = BOTS[args.bot]
    bot_main = import_module(cfg.module).main
    run_loop(args.minutes, bot_main, args.date)


if __name__ == "__main__":
    main()
