from typing import Self
from enum import Enum


class InputEventType(Enum):
    EMPTY = 1
    CHAR = 2
    ESCAPE = 3
    TAB = 4
    ENTER = 5
    BACKSPACE = 6


class InputEvent:
    @classmethod
    def EMPTY(cls) -> Self:
        return cls(InputEventType.EMPTY)

    @classmethod
    def ESCAPE(cls) -> Self:
        return cls(InputEventType.ESCAPE)

    @classmethod
    def TAB(cls) -> Self:
        return cls(InputEventType.TAB)

    @classmethod
    def ENTER(cls) -> Self:
        return cls(InputEventType.ENTER)

    @classmethod
    def BACKSPACE(cls) -> Self:
        return cls(InputEventType.BACKSPACE)

    @classmethod
    def CHAR(cls, char: str) -> Self:
        return cls(InputEventType.CHAR, char)


    
    def __init__(self, type: InputEventType, char: str = "") -> None:
        self.type: InputEventType = type
        self.char: str = char
