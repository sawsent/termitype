from enum import Enum
from dataclasses import dataclass
from typing import Dict


class TestStyle(Enum):
    BLOCK = "block"
    SINGLE_LINE_FOLLOW = "line"

class SettingType(Enum):
    FREE = "FREE"
    OPTIONS = "OPTIONS"

@dataclass
class Settings():
    width: int = 100
    height: int = 30
    language: str = "english"
    test_word_count: int = 50
    test_text_max_width: int = 60
    show_exit_message: bool = True
    display_outline: bool = True
    show_logo: bool = True

    def descriptions(self) -> Dict:
        return {
            "display": {
                "width": {
                    "value": self.width,
                    "desc": "The width of the display (terminal columns)",
                    "type": SettingType.FREE
                },
                "height": {
                    "value": self.height,
                    "desc": "The height of the display (terminal lines)",
                    "type": SettingType.FREE
                },
                "outline": {
                    "value": self.display_outline,
                    "desc": "Show the outline of the display",
                    "type": SettingType.OPTIONS,
                    "options": ["show","hide"]
                },
            },
            "typing": {
                "language": {
                    "value": self.language,
                    "desc": "The language to take words from (should be in data/languages)",
                    "type": SettingType.FREE
                },
                "words": {
                    "value": self.test_word_count,
                    "desc": "Amount of words on each test",
                    "type": SettingType.FREE
                },
                "max_width": {
                    "value": self.test_text_max_width,
                    "desc": "Max width of the test text on test run",
                    "type": SettingType.FREE
                },
            },
            "general": {
                "exit_message": {
                    "value": self.show_exit_message,
                    "desc": "Display the exit message on quit",
                    "type": SettingType.OPTIONS,
                    "options": ["show","hide"]
                },
                "show_logo": {
                    "value": self.show_logo,
                    "desc": "Display the termitype logo",
                    "type": SettingType.OPTIONS,
                    "options": ["show","hide"]
                }
            }
        }

