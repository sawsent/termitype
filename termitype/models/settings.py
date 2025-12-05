from enum import Enum
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
    show_exit_message: bool = True
    display_outline: bool = True

