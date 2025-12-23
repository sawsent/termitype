import re
from termitype.models.color import Color, Bg

# Matches ANY ANSI SGR sequence (foreground, background, bold, etc.)
_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")

def color(text: str, fg: Color | None = None, bg: Bg | None = None, reset: str | None = None) -> str:
    """
    Apply foreground and/or background ANSI color codes.
    Resets the style at the end to the configured theme base_color.
    """
    codes = []

    if fg is not None:
        codes.append(str(fg.value))
    if bg is not None:
        codes.append(str(bg.value))

    if not codes:
        return text

    r = reset or "0"

    start = f"\x1b[{';'.join(codes)}m"
    end = f"\x1b[{r}m"

    return f"{start}{text}{end}"


def removed_color(text: str) -> str:
    """Strip all ANSI color escape sequences."""
    return _ANSI_RE.sub("", text)


def visible_len(s: str) -> int:
    """The length of the string as it appears in the terminal (no ANSI codes)."""
    return len(removed_color(s))

