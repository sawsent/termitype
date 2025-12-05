from typing import Optional, Self
from enum import Enum
from typing import Dict, List
from termitype.models.presentation.cursor import Cursor
from termitype.models.presentation.highlight import Highlight
from math import floor, ceil

from termitype.utils.color import Bg, Color, color, visible_len as v_len

def outline(lines: List[str]) -> List[str]:
    width = v_len(lines[0]) if lines else 0
    return [ f"┌{"─" * width}┐" ] + [ f"│{l}│" for l in lines ] + [ f"└{"─" * width}┘" ]

def pad(lines: List[str], amount: int) -> List[str]:
    p = " " * amount
    return [ p + line + p for line in lines ]

def filler(amount: int, filler_char: str = " ") -> str:
        return filler_char * amount


class LineStyle:
    DINAMIC = -1
    IGNORE = -2

    CENTER: int = 0
    ALIGN_LEFT: int = 1 
    ALIGN_RIGHT: int = 2

    @classmethod
    def CENTERED(cls, padding: int = 0, outlined: bool = False) -> Self:
        return cls(cls.CENTER, padding, padding, cls.DINAMIC, outlined)

    @classmethod
    def ALIGNED_LEFT(cls, padding_left: int = 0, gap: int = 1, outlined: bool = False) -> Self:
        return cls(cls.ALIGN_LEFT, padding_left, cls.IGNORE, gap, outlined)

    @classmethod
    def ALIGNED_RIGHT(cls, padding_right: int = 0, gap: int = 1, outlined: bool = False) -> Self:
        return cls(cls.ALIGN_RIGHT, cls.IGNORE, padding_right, gap, outlined)

    def __init__(self, style_id: int, padding_left: int, padding_right: int, gap: int, outlined: bool) -> None:
        self.id: int = style_id
        self.padding_left: int = padding_left
        self.padding_right: int = padding_right
        self.gap: int = gap
        self.outlined: bool = outlined

class Line:
    @classmethod
    def EMPTY(cls) -> Self:
        return cls([""], LineStyle.CENTERED(), None, None)

    @classmethod
    def CENTERED(cls, text: str) -> Self:
        return cls([text], LineStyle.CENTERED(), None, None)

    @classmethod
    def CENTER(cls, elements: List[str], padding: int = 0, color: Optional[Color] = None, bg: Optional[Bg] = None, outlined: bool = False) -> Self:
        return cls(elements, LineStyle.CENTERED(padding=padding, outlined=outlined), color, bg)

    @classmethod
    def ALIGNED_LEFT(cls, elements: List[str], padding_left: int, gap: int, outlined: bool = False, color: Color | None = None, bg: Bg | None = None) -> Self:
        return cls(elements, LineStyle.ALIGNED_LEFT(padding_left, gap, outlined), color, bg)

    @classmethod
    def CENTERED_LINES(cls, lines: List[str]) -> List[Self]:
        return [cls.CENTERED(line) for line in lines]

    def __init__(self, elements: List[str], style: LineStyle, color: Optional[Color], bg: Optional[Bg]):
        self.elements: List[str] = elements
        self.style: LineStyle = style
        self.bg: Optional[Bg] = bg
        self.color: Optional[Color] = color

    def as_text(self, total_width: int) -> List[str]:
        if self.style.outlined:
            return outline([self.without_outline_text(total_width - 2)])
        else:
            return [self.without_outline_text(total_width)]

    def without_outline_text(self, total_width: int) -> str:
        if len(self.elements) == 0:
            return filler(total_width)
        match self.style.id:
            case LineStyle.CENTER:
                if len(self.elements) == 1:
                    half_filler = (total_width - v_len(self.elements[0])) / 2
                    return filler(floor(half_filler)) + self.elements[0] + filler(ceil(half_filler))
                empty_space = total_width - sum([v_len(element) for element in self.elements]) - self.style.padding_right - self.style.padding_left
                space_between = filler(floor(empty_space / (len(self.elements) - 1)))
                without_padding = color(space_between.join(self.elements), self.color, self.bg)
                return filler(self.style.padding_left) + without_padding + filler(total_width - self.style.padding_left - v_len(without_padding))
            case LineStyle.ALIGN_LEFT:
                space_between = " " * self.style.gap
                without_padding = color(space_between.join(self.elements), self.color, self.bg)
                return filler(self.style.padding_left) + without_padding + filler(total_width - self.style.padding_left - v_len(without_padding))
            case LineStyle.ALIGN_RIGHT:
                space_between = " " * self.style.gap
                without_padding = color(space_between.join(self.elements), self.color, self.bg)
                return filler(total_width - self.style.padding_right - v_len(without_padding)) + without_padding + filler(self.style.padding_right)

        return filler(total_width)


class Bar:
    @classmethod
    def EMPTY(cls) -> Self:
        return cls([], False, LineStyle.CENTERED())

    @classmethod
    def SINGLE(cls, elements: List[str], show_outline: bool = False, style: LineStyle = LineStyle.CENTERED()) -> Self:
        return cls([elements], show_outline, style)

    @classmethod
    def MULTIPLE(cls, lines: List[List[str]], show_outline: bool = False, style: LineStyle = LineStyle.CENTERED()) -> Self:
        return cls(lines, show_outline, style)

    def __init__(self, lines: List[List[str]], show_outline: bool, style: LineStyle):
        self.lines: List[List[str]] = lines
        self.show_outline: bool = show_outline
        self.style: LineStyle = style

    @property
    def height(self) -> int:
        return len(self.lines) + (4 if self.show_outline else 0)

    def get_lines(self, total_width: int) -> List[str]:
        if not self.show_outline: return [ self.line_as_text(line, total_width) for line in self.lines ]
        without_padding = outline([ self.line_as_text(line, total_width - 4) for line in self.lines ])
        return pad(without_padding, 1)


    def line_as_text(self, line: List[str], total_width: int) -> str:
        if len(line) == 0:
            return filler(total_width)
        match self.style.id:
            case LineStyle.CENTER:
                if len(line) == 1:
                    half_filler = (total_width - v_len(line[0])) / 2
                    return filler(floor(half_filler)) + line[0] + filler(ceil(half_filler))
                empty_space = total_width - sum([v_len(element) for element in line]) - self.style.padding_right - self.style.padding_left
                space_between = filler(floor(empty_space / (len(line) - 1)))
                without_padding = space_between.join(line)
                return filler(self.style.padding_left) + without_padding + filler(total_width - self.style.padding_left - v_len(without_padding))
            case LineStyle.ALIGN_LEFT:
                space_between = " " * self.style.gap
                without_padding = space_between.join(line)
                return filler(self.style.padding_left) + without_padding + filler(total_width - self.style.padding_left - v_len(without_padding))
            case LineStyle.ALIGN_RIGHT:
                space_between = " " * self.style.gap
                without_padding = space_between.join(line)
                return filler(total_width - self.style.padding_right - v_len(without_padding)) + without_padding + filler(self.style.padding_right)

        return filler(total_width)
        

class SlideStyle(Enum):
    CENTERED_Y = 1
    ALIGNED_TOP = 2
    ALIGNED_BOTTOM = 3

class Slide:

    @classmethod
    def CENTERED_XY(cls, lines: List[str], outlined: bool = False) -> Self:
        return cls(Line.CENTERED_LINES(lines), SlideStyle.CENTERED_Y, outlined=outlined)

    @classmethod
    def CENTERED(cls, lines: List[Line], outlined: bool = False) -> Self:
        return cls(lines, SlideStyle.CENTERED_Y, outlined=outlined)

    @classmethod
    def ALIGNED_TOP(cls, lines: List[Line], outlined: bool = False, padding: int = 0) -> Self:
        return cls(lines, SlideStyle.ALIGNED_TOP, outlined=outlined, padding=padding)

    @classmethod
    def ALIGNED_BOTTOM(cls, lines: List[Line], outlined: bool = False, padding: int = 0) -> Self:
        return cls(lines, SlideStyle.ALIGNED_BOTTOM, outlined=outlined, padding=padding)

    def __init__(self, lines: List[Line], style: SlideStyle, outlined: bool, padding: int = 0):
        self.lines: List[Line] = lines
        self.style: SlideStyle = style
        self.outlined: bool = outlined
        self.padding: int = padding

class Presentation:
    def __init__(self,
                 width: int,
                 height: int,
                 slide: Slide,
                 top_bar: Bar = Bar.EMPTY(),
                 bottom_bar: Bar = Bar.EMPTY(),
                 highlights: List[Highlight] = [],
                 cursor: Cursor = Cursor.HIDDEN(),
                 show_outline: bool = True,
                 meta: Dict = {}) -> None:
        self.width = width
        self.height = height
        self.slide: Slide = slide
        self.cursor: Cursor = cursor
        self.top_bar: Bar = top_bar
        self.bottom_bar: Bar = bottom_bar
        self.highlights: List[Highlight] = highlights
        self.show_outline: bool = show_outline
        self.meta: Dict = meta

    def as_text(self) -> str:
        outlined_slide = pad(outline(self.align_slide()), 1) if self.slide.outlined else self.align_slide()
        without_outline = self.top_bar.get_lines(self.width) + outlined_slide + self.bottom_bar.get_lines(self.width)
        if self.show_outline:
            text = "\n".join(outline(without_outline))
        else:
            text = "\n".join(without_outline)
        return text

    def align_slide(self) -> List[str]:
        text_lines = self.get_text_from_lines()
        filler_lines_len = self.height - self.bottom_bar.height - self.top_bar.height - len(text_lines)
        match self.slide.style:
            case SlideStyle.ALIGNED_TOP:
                return self.filler_lines(self.slide.padding) + text_lines + self.filler_lines(filler_lines_len - self.slide.padding)
            case SlideStyle.ALIGNED_BOTTOM:
                return self.filler_lines(filler_lines_len - self.slide.padding) + text_lines + self.filler_lines(self.slide.padding)
            case SlideStyle.CENTERED_Y:
                return self.filler_lines(floor(filler_lines_len / 2)) + text_lines + self.filler_lines(ceil(filler_lines_len / 2))


    def filler_lines(self, amount: int) -> List[str]:
        return [ filler(self.width) for _ in range(amount) ]

    def get_text_from_lines(self) -> List[str]:
        return [a for line in self.slide.lines for a in line.as_text(self.width)]

