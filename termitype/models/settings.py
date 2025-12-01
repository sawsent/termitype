from typing import Self
from dataclasses import dataclass

@dataclass
class Settings():
    width: int = 150
    height: int = 40

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
