from typing import Self
from enum import Enum
from typing import Dict, List
from termitype.models.presentation.cursor import Cursor
from termitype.models.presentation.highlight import Highlight
from math import floor, ceil

from termitype.utils.color import visible_len

def filler(amount: int, filler_char: str = " ") -> str:
        return filler_char * amount

class LineStyle(Enum):
    CENTERED = 1
    ALIGNED_LEFT = 2
    ALIGNED_RIGHT = 3

class Line:
    @classmethod
    def EMPTY(cls) -> Self:
        return cls("", LineStyle.CENTERED)

    @classmethod
    def CENTERED(cls, text: str) -> Self:
        return cls(text, LineStyle.CENTERED)

    @classmethod
    def CENTERED_LINES(cls, lines: List[str]) -> List[Self]:
        return [cls.CENTERED(line) for line in lines]

    def __init__(self, text: str, style: LineStyle):
        self.text: str = text
        self.style: LineStyle = style

class Bar:
    @classmethod
    def EMPTY(cls) -> Self:
        return cls([], 0)

    def __init__(self, elements: List[str], width: int):
        self.elements: List[str] = elements
        self.width: int = width
        self.text: str = self.__text()

    def __text(self) -> str:
        if len(self.elements) == 0:
            return ""
        elif len(self.elements) == 1:
            return self.elements[0]
        empty_space = self.width - sum([len(element) for element in self.elements])
        space_between = filler(floor(empty_space / (len(self.elements) - 1)))
        return space_between.join(self.elements)


class SlideStyle(Enum):
    CENTERED_Y = 1
    ALIGNED_TOP = 2
    ALIGNED_BOTTOM = 3

class Slide:

    @classmethod
    def CENTERED_XY(cls, lines: List[str]) -> Self:
        return cls(Line.CENTERED_LINES(lines), SlideStyle.CENTERED_Y)

    @classmethod
    def CENTERED(cls, lines: List[Line]) -> Self:
        return cls(lines, SlideStyle.CENTERED_Y)

    def __init__(self, lines: List[Line], style: SlideStyle):
        self.lines: List[Line] = lines
        self.style: SlideStyle = style

class Presentation:
    def __init__(self,
                 width: int,
                 height: int,
                 slide: Slide,
                 top_bar: Bar = Bar.EMPTY(),
                 bottom_bar: Bar = Bar.EMPTY(),
                 highlights: List[Highlight] = [],
                 cursor: Cursor = Cursor.HIDDEN(),
                 meta: Dict = {}) -> None:
        self.width = width
        self.height = height
        self.slide: Slide = slide
        self.cursor: Cursor = cursor
        self.top_bar: Bar = top_bar
        self.bottom_bar: Bar = bottom_bar
        self.highlights: List[Highlight] = highlights
        self.meta: Dict = meta

    def as_text(self) -> str:
        return "\n".join([self.align_line(Line.CENTERED(self.top_bar.text))] + self.align_slide() + [self.align_line(Line.CENTERED(self.bottom_bar.text))])

    def align_slide(self) -> List[str]:
        text_lines = self.get_text_from_lines()
        filler_lines_len = self.height - 2 - len(text_lines)
        match self.slide.style:
            case SlideStyle.ALIGNED_TOP:
                return text_lines + self.filler_lines(filler_lines_len)
            case SlideStyle.ALIGNED_BOTTOM:
                return self.filler_lines(filler_lines_len) + text_lines
            case SlideStyle.CENTERED_Y:
                return self.filler_lines(floor(filler_lines_len / 2)) + text_lines + self.filler_lines(ceil(filler_lines_len / 2))


    def filler_lines(self, amount: int) -> List[str]:
        return [ filler(self.width) for _ in range(amount) ]

    def get_text_from_lines(self) -> List[str]:
        return [ self.align_line(line) for line in self.slide.lines ]
        
    def align_line(self, line: Line) -> str:
        total_filler_amount = self.width - visible_len(line.text)
        total_filler = filler(total_filler_amount)
        match line.style:
            case LineStyle.ALIGNED_LEFT:
                return line.text + total_filler
            case LineStyle.ALIGNED_RIGHT:
                return total_filler + line.text
            case LineStyle.CENTERED:
                return filler((floor(total_filler_amount / 2))) + line.text + filler((ceil(total_filler_amount / 2)))


