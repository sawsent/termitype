from typing import Self
from enum import Enum


class CursorStyle(Enum):
    HIDDEN = 1
    THICK = 2
    THIN = 3
    BLOCK = 4

    @classmethod
    def get_repr(cls, style: Self) -> str:
        return {
            1: "",
            2: "┃",
            3: "|",
            4: "█"
        }[style._value_]
    

class Cursor:

    @classmethod
    def HIDDEN(cls) -> Self:
        return cls(CursorStyle.HIDDEN)

    @classmethod
    def THICK(cls, line: int, col: int) -> Self:
        return cls(CursorStyle.THICK, line = line, col = col)

    @classmethod
    def THIN(cls, line: int, col: int) -> Self:
        return cls(CursorStyle.THIN, line = line, col = col)

    @classmethod
    def BLOCK(cls, line: int, col: int) -> Self:
        return cls(CursorStyle.BLOCK, line = line, col = col)

    def __init__(self, style: CursorStyle, line: int = 0, col: int = 0):
        self.line: int = line
        self.col: int = col
        self.style: CursorStyle = style

    
