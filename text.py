"""Functions and utilities for displaying text."""

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


def display_line(body: str) -> None:
    """Displays a line of text to the user. Adds a linebreak."""
    print(body, flush=True)


def unconceal() -> None:
    """Unconceals the current line from the terminal."""
    display_span("\033[28m")


def warn(body: str) -> str:
    """Wraps text in ANSI sequences to highlight it as a warning."""
    return f"{WARN}{body}{RESET}"
