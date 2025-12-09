from enum import Enum
from dataclasses import dataclass
from typing import Dict, Self

def to_display(x) -> str:
    if isinstance(x, bool):
        return "on" if x else "off"
    elif isinstance(x, int):
        return f"{x}"
    elif isinstance(x, str):
        return x
    else:
        return str(x)

def to_int(s: str, default: int) -> int:
    ret = default
    try:
        ret = int(s)
    finally:
        return ret

def to_bool(s: str) -> bool:
    return s == "on"

class TestStyle(Enum):
    BLOCK = "block"
    SINGLE_LINE_FOLLOW = "line"

class SettingType(Enum):
    FREE = "FREE"
    OPTIONS = "OPTIONS"

class Settings:
    def __init__(
        self,
        width: int = 100,
        height: int = 30,
        language: str = "english",
        test_word_count: int = 50,
        test_text_max_width: int = 60,
        show_exit_message: bool = True,
        display_outline: bool = True,
        show_logo: bool = True
    ) -> None:
        self.width: int = width
        self.height: int = height
        self.language: str = language
        self.test_word_count: int = test_word_count
        self.test_text_max_width: int = test_text_max_width
        self.show_exit_message: bool = show_exit_message
        self.display_outline: bool = display_outline
        self.show_logo: bool = show_logo


    @classmethod
    def from_descriptions(cls, descs: Dict, previous: Self) -> Self:
        return cls(
            width = to_int(descs["display"]["width"]["value"], previous.width),
            height = to_int(descs["display"]["height"]["value"], previous.height),
            display_outline = to_bool(descs["display"]["outline"]["value"]),
            language = descs["typing"]["language"]["value"],
            test_word_count = to_int(descs["typing"]["words"]["value"], previous.test_word_count),
            test_text_max_width = to_int(descs["typing"]["max_width"]["value"], previous.test_text_max_width),
            show_exit_message = to_bool(descs["general"]["exit_message"]["value"]),
            show_logo = to_bool(descs["general"]["show_logo"]["value"]),
        )

    def descriptions(self) -> Dict:
        return {
            "display": {
                "width": {
                    "value": to_display(self.width),
                    "desc": "The width of the display (terminal columns)",
                    "type": SettingType.FREE,
                    "index": 0
                },
                "height": {
                    "value": to_display(f"{self.height}"),
                    "desc": "The height of the display (terminal lines)",
                    "type": SettingType.FREE,
                    "index": 1
                },
                "outline": {
                    "value": to_display(self.display_outline),
                    "desc": "Show the outline of the display",
                    "type": SettingType.OPTIONS,
                    "options": ["on","off"],
                    "index": 2
                },
            },
            "typing": {
                "language": {
                    "value": to_display(self.language),
                    "desc": "The language to take words from (should be in data/languages)",
                    "type": SettingType.FREE,
                    "index": 3
                },
                "words": {
                    "value": to_display(self.test_word_count),
                    "desc": "Amount of words on each test",
                    "type": SettingType.FREE,
                    "index": 4
                },
                "max_width": {
                    "value": to_display(self.test_text_max_width),
                    "desc": "Max width of the test text on test run",
                    "type": SettingType.FREE,
                    "index": 5
                },
            },
            "general": {
                "exit_message": {
                    "value": to_display(self.show_exit_message),
                    "desc": "Display the exit message on quit",
                    "type": SettingType.OPTIONS,
                    "options": ["on","off"],
                    "index": 6
                },
                "show_logo": {
                    "value": to_display(self.show_logo),
                    "desc": "Display the termitype logo",
                    "type": SettingType.OPTIONS,
                    "options": ["on","off"],
                    "index": 7
                },
            }
        }

    @property
    def max_setting_index(self) -> int:
        return 7

