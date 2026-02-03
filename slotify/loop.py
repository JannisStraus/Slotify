import html
import time
import traceback
from datetime import datetime
from typing import Callable, TypeVar

from slotify.bot import send_markdown

P = TypeVar("P")


def sleep_duration(minutes: int = 10, seconds: int = 0) -> float:
    """
    Calculate the sleep duration until the next multiple of the specified period.

    The period is defined by a combination of minutes and seconds.
    For example, with minutes=0 and seconds=10, the function waits until the next 10-second mark.

    Args:
        minutes (int): Number of minutes in the period.
        seconds (int): Number of seconds in the period.

    Returns:
        float: The number of seconds to sleep.
    """
    total_period = minutes * 60 + seconds
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


def short_exc(e: BaseException, frames: int = 1) -> str:
    """
    Return a compact markdown block with the exception type, message
    and the last `frames` stack frames.
    """
    head = f"*{e.__class__.__name__}*: {html.escape(str(e))}"

    tb = traceback.extract_tb(e.__traceback__)
    last_frames = tb[-frames:]
    stack = "\n".join(
        f"`{f.filename}:{f.lineno}` - {f.name} ➜ {(f.line or 'Empty').strip()}"
        for f in last_frames
    )
    return f"{head}\n{stack}"


def run_loop(minutes: int, func: Callable[[P], str | None], params: P) -> None:
    while True:
        try:
            text = func(params)
            if text:
                send_markdown(text)
        except Exception as e:
            try:
                print(f"{type(e).__name__}: {e}")
                send_markdown(f"{type(e).__name__}: {e}")
            except Exception as e:
                print(f"`send_markdown(short_exc(e)` failed: {type(e).__name__}: {e}")
        time.sleep(sleep_duration(minutes))
