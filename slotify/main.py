import argparse

from slotify.loop import run_loop
from slotify.morante.main import main as morante_main
from slotify.wellnest.main import main as wellnest_main


def main() -> None:
    parser = argparse.ArgumentParser(description="Slotify: Search for available slots.")
    subparsers = parser.add_subparsers(dest="bot", required=True, help="Bot to run")

    # Morante bot
    morante_parser = subparsers.add_parser("morante", help="Morante Hair Salon bot")
    morante_parser.add_argument(
        "-m",
        "--minutes",
        type=int,
        default=5,
        help="Number of minutes to wait between checks (default: 5).",
    )
    morante_parser.add_argument(
        "-d",
        "--days",
        type=int,
        required=True,
        help="Number of days in advance for which to search for available slots.",
    )

    # Wellnest bot
    wellnest_parser = subparsers.add_parser("wellnest", help="Wellnest bot")
    wellnest_parser.add_argument(
        "-m",
        "--minutes",
        type=int,
        default=5,
        help="Number of minutes to wait between checks (default: 5).",
    )
    wellnest_parser.add_argument(
        "-d",
        "--date",
        type=str,
        required=True,
        help="Date (DD.MM.YYYY or YYYY-MM-DD) to search for available slots.",
    )

    args = parser.parse_args()

    if args.bot == "morante":
        run_loop(args.minutes, morante_main, args.days)
    elif args.bot == "wellnest":
        run_loop(args.minutes, wellnest_main, args.date)


if __name__ == "__main__":
    main()
