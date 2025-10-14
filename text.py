"""Functions and utilities for displaying text."""

import time
from typing import Iterator

RESET = "\033[0m"
WARN = "\033[41;3;1m"


def clear_previous_line() -> None:
    """Clears the previous line from the terminal."""
    clear_previous_lines(1)


def conceal() -> None:
    """Conceals the current line from the terminal."""
    display_span("\033[8m")


def clear_previous_lines(n: int) -> None:
    """Clears the previous n lines from the terminal."""
    for _ in range(n):
        display_span("\033[F\033[K")  # Move cursor up and clear line


def display_span(body: str) -> None:
    """Displays a span of text to the user. Does not add a linebreak."""
    print(body, end="", flush=True)


def linebreak() -> None:
    """Displays a linebreak to the user."""
    display_line("")


def exponential_increase(num: int,
                         start: int | float = 1,
                         increase: float = 0.05) -> Iterator[float]:
    """An iterator that yields exponentially increasing values."""
    current = start
    for i in range(1, num + 1):
        yield current
        current *= (1 + increase)


def display_line(body: str) -> None:
    """Displays a line of text to the user. Adds a linebreak."""
    print(body, flush=True)


def erase_line() -> None:
    """Erases the current line from the terminal."""
    display_span("\033[K")


def pause(delay: int | float) -> None:
    """Pauses for a given number of seconds."""
    time.sleep(delay)


def pause_short() -> None:
    """Pauses for a short moment."""
    pause(0.5)


def pause_medium() -> None:
    """Pauses for a medium moment."""
    pause(1.0)


def pause_long() -> None:
    """Pauses for a long moment."""
    pause(2.0)


def pause_extra_long() -> None:
    """Pauses for an extra long moment."""
    pause(4.0)


def unconceal() -> None:
    """Unconceals the current line from the terminal."""
    display_span("\033[28m")
    linebreak()


def wait_visible(seconds: int | float, *, char: str = ".", interval: float = 1.0) -> None:
    """Waits for a number of seconds, displaying a character each second."""
    awaited = 0
    while awaited < seconds:
        time.sleep(interval)
        display_span(char)
        awaited += interval
    linebreak()


def warn(body: str) -> str:
    """Wraps text in ANSI sequences to highlight it as a warning."""
    return f"{WARN}{body}{RESET}"
