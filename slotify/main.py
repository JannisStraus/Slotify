import argparse
from importlib import import_module

from slotify.loop import run_loop

BOTS = {
    "morante": {
        "help": "Morante Hair Salon bot",
        "arg": (
            "-d",
            "--days",
            {
                "type": int,
                "required": True,
                "help": "Number of days in advance for which to search for available slots.",
            },
        ),
        "module": "slotify.morante.main",
        "param": "days",
    },
    "wellnest": {
        "help": "Wellnest bot",
        "arg": (
            "-d",
            "--date",
            {
                "type": str,
                "required": True,
                "help": "Date (DD.MM.YYYY or YYYY-MM-DD) to search for available slots.",
            },
        ),
        "module": "slotify.wellnest.main",
        "param": "date",
    },
    "mywellness": {
        "help": "MyWellness bot",
        "arg": (
            "-d",
            "--date",
            {
                "type": str,
                "required": True,
                "help": "Date (DD.MM.YYYY or YYYY-MM-DD) to search for available slots.",
            },
        ),
        "module": "slotify.mywellness.main",
        "param": "date",
    },
    "justiz": {
        "help": "Justiz bot",
        "arg": (
            "-d",
            "--date",
            {
                "type": str,
                "required": True,
                "help": "Date (DD.MM.YYYY or YYYY-MM-DD) to search for available slots.",
            },
        ),
        "module": "slotify.justiz.main",
        "param": "date",
    },
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Slotify: Search for available slots.")
    subparsers = parser.add_subparsers(dest="bot", required=True, help="Bot to run")

    for name, cfg in BOTS.items():
        sub = subparsers.add_parser(name, help=cfg["help"])
        sub.add_argument(
            "-m",
            "--minutes",
            type=int,
            default=5,
            help="Number of minutes to wait between checks (default: 5).",
        )
        flag_short, flag_long, kwargs = cfg["arg"]
        sub.add_argument(flag_short, flag_long, **kwargs)

    args = parser.parse_args()
    cfg = BOTS[args.bot]
    bot_main = import_module(cfg["module"]).main
    run_loop(args.minutes, bot_main, getattr(args, cfg["param"]))


if __name__ == "__main__":
    main()
