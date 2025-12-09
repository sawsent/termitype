from enum import Enum
import re

# Matches ANY ANSI SGR sequence (foreground, background, bold, etc.)
_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")

class Color(Enum):
    RESET = 0

    # Foreground colors
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37

    # Bright foreground
    BRIGHT_BLACK = 90
    BRIGHT_RED = 91
    BRIGHT_GREEN = 92
    BRIGHT_YELLOW = 93
    BRIGHT_BLUE = 94
    BRIGHT_MAGENTA = 95
    BRIGHT_CYAN = 96
    BRIGHT_WHITE = 97

class Bg(Enum):
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    MAGENTA = 45
    CYAN = 46
    WHITE = 47

    BRIGHT_BLACK = 100
    BRIGHT_RED = 101
    BRIGHT_GREEN = 102
    BRIGHT_YELLOW = 103
    BRIGHT_BLUE = 104
    BRIGHT_MAGENTA = 105
    BRIGHT_CYAN = 106
    BRIGHT_WHITE = 107


def color(text: str, fg: Color | None = None, bg: Bg | None = None) -> str:
    """
    Apply foreground and/or background ANSI color codes.
    Resets the style at the end.
    """
    codes = []

    if fg is not None:
        codes.append(str(fg.value))
    if bg is not None:
        codes.append(str(bg.value))

    if not codes:
        return text  # no color applied

    start = f"\x1b[{';'.join(codes)}m"
    end = "\x1b[0m"

    return f"{start}{text}{end}"


def removed_color(text: str) -> str:
    """Strip all ANSI color escape sequences."""
    return _ANSI_RE.sub("", text)


def visible_len(s: str) -> int:
    """The length of the string as it appears in the terminal (no ANSI codes)."""
    return len(removed_color(s))

