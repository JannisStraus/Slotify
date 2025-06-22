import time
from datetime import datetime

from slotify.bot import send
from slotify.parser import parse_agenda
from slotify.webscraper import search_slot


def sleep_duration(period_minutes: int = 0, period_seconds: int = 10) -> float:
    """
    Calculate the sleep duration until the next multiple of the specified period.

    The period is defined by a combination of minutes and seconds.
    For example, with period_minutes=0 and period_seconds=10, the function waits until the next 10-second mark.

    Args:
        period_minutes (int): Number of minutes in the period.
        period_seconds (int): Number of seconds in the period.

    Returns:
        float: The number of seconds to sleep.
    """
    total_period = period_minutes * 60 + period_seconds
    if total_period <= 0:
        raise ValueError("The total period must be greater than zero.")

    now = datetime.now()
    # Convert current time into seconds since midnight (including fractional seconds)
    seconds_since_midnight = (
        now.hour * 3600 + now.minute * 60 + now.second + now.microsecond / 1_000_000
    )
    # Find how far along we are in the current period
    remainder = seconds_since_midnight % total_period
    # If exactly at a period boundary, wait for the full period; otherwise, wait until the boundary.
    sleep_time = total_period - remainder if remainder else total_period
    return sleep_time


def run_loop() -> None:
    while True:
        time.sleep(sleep_duration(5, 0))
        html = search_slot()
        slots = parse_agenda(html, 10)
        send(slots)
