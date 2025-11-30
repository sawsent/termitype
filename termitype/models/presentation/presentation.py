from typing import Dict, List
from termitype.models.presentation.cursor import Cursor
from termitype.models.presentation.highlight import Highlight

class Presentation:
    def __init__(self, lines: List[str], highlights: List[Highlight] = [], cursor: Cursor = Cursor.HIDDEN(), meta: Dict = {}) -> None:
        self.cursor: Cursor = cursor
        self.lines: List[str] = lines
        self.highlights: List[Highlight] = highlights
        self.meta: Dict = meta

