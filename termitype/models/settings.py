from enum import Enum
from typing import Self
from dataclasses import dataclass


class TestStyle(Enum):
    BLOCK = "BLOCK"
    SINGLE_LINE_FOLLOW = "SINGLE"

@dataclass
class Settings():
    width: int = 100
    height: int = 30
    language: str = "english"
    test_word_count: int = 50
    test_text_max_width: int = 60
    test_style: TestStyle = TestStyle.BLOCK
    ahead: int = 2
    behind: int = 2

@dataclass(frozen=True)
class DisplaySettings():
    width: int
    height: int

    @classmethod
    def from_settings(cls, settings: Settings) -> Self:
        return cls(
            width = settings.width,
            height = settings.height
        )

@dataclass
class TypingRunSettings():
    words: int
    test_text_max_width: int

    @classmethod
    def from_settings(cls, settings: Settings) -> Self:
        return cls(
            words = settings.test_word_count,
            test_text_max_width = settings.test_text_max_width
        )

