from typing import Self
from dataclasses import dataclass

@dataclass
class Settings():
    width: int = 150
    height: int = 40
    test_word_count: int = 10

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

    @classmethod
    def from_settings(cls, settings: Settings) -> Self:
        return cls(
            words = settings.test_word_count
        )
