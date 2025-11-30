from dataclasses import dataclass
from typing import Dict
from enum import Enum


class HighlightType(Enum):
    COLOR = 1
    BACKGROUND = 2


@dataclass
class Highlight:
    line_idx: int
    start_col: int
    end_col: int
    highlight_type: HighlightType
    info: Dict
    
    

