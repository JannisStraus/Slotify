import argparse

from slotify.loop import run_loop


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Continuously search for available slots at Morante Hair Salon."
    )
    parser.add_argument(
        "-m",
        "--minutes",
        default=5,
        type=int,
        required=False,
        help="Number of minutes to wait between checks (default: 5).",
    )
    parser.add_argument(
        "-s",
        "--seconds",
        default=0,
        type=int,
        required=False,
        help="Additional seconds to wait between checks (default: 0).",
    )
    parser.add_argument(
        "-d",
        "--days",
        type=int,
        required=False,
        help="Number of days in advance for which to search for available slots.",
    )
    args = parser.parse_args()

    run_loop(args.minutes, args.seconds, args.days)


if __name__ == "__main__":
    main()
