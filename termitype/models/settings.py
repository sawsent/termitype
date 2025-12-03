from typing import Self
from dataclasses import dataclass

@dataclass
class Settings():
    width: int = 100
    height: int = 30
    test_word_count: int = 50
    test_text_max_width: int = 60

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

