from enum import Enum
import re


_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")

class Color(Enum):
    RESET = 0
    RED = 31
    GREEN = 32
    YELLOW = 33
    CYAN = 36
    WHITE = 37
    BRIGHT_BLACK = 90
    BRIGHT_WHITE = 97

def color(text: str, color: Color) -> str:
    return f"\x1b[{color.value}m{text}\x1b[0m"

def removed_color(text: str) -> str:
    return _ANSI_RE.sub("", text)

def visible_len(s: str) -> int:
    return len(removed_color(s))
