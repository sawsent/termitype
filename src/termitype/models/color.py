from enum import Enum

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

    @classmethod
    def from_string(cls, string: str) -> "Color":
        match string:
            case "BLACK":
                return Color.BLACK 
            case "RED":
                return Color.RED 
            case "GREEN":
                return Color.GREEN 
            case "YELLOW":
                return Color.YELLOW 
            case "BLUE":
                return Color.BLUE 
            case "MAGENTA":
                return Color.MAGENTA 
            case "CYAN":
                return Color.CYAN 
            case "WHITE":
                return Color.WHITE 
            case "BRIGHT_BLACK":
                return Color.BRIGHT_BLACK 
            case "BRIGHT_RED":
                return Color.BRIGHT_RED 
            case "BRIGHT_GREEN":
                return Color.BRIGHT_GREEN 
            case "BRIGHT_YELLOW":
                return Color.BRIGHT_YELLOW 
            case "BRIGHT_BLUE":
                return Color.BRIGHT_BLUE 
            case "BRIGHT_MAGENTA":
                return Color.BRIGHT_MAGENTA 
            case "BRIGHT_CYAN":
                return Color.BRIGHT_CYAN 
            case "BRIGHT_WHITE":
                return Color.BRIGHT_WHITE 
            case c:
                raise RuntimeError(f"{c} is not a valid color.")


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


