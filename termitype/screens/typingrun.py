from termitype.core.engine import TypingEngine
from termitype.models.engine.run import RunSegment, SegmentType
from termitype.models.inputevent import InputEvent, InputEventType as IET
from termitype.models.presentation.presentation import Bar, Presentation, Line, Slide
from termitype.models.settings import DisplaySettings
from termitype.screens.base import Screen
from termitype.adapters.base import Adapter
from typing import Optional, override, List, Self

from termitype.utils.color import Color, color, visible_len

class TypingRunScreen(Screen):

    def __init__(self, adapter: Adapter, menu: Screen, typing_engine: TypingEngine, settings: DisplaySettings):
        super().__init__(settings)
        self.adapter: Adapter = adapter
        self.__return_to: Screen = menu
        self.engine = typing_engine
        self.word_count = 50
        self.restart()

    @override
    def restart(self) -> Self:
        self.last_key_press: str = ""
        self.is_to_return: bool = False
        self.__next_screen: Optional[Screen] = self
        self.engine.new_run(self.word_count)
        return self


    @override
    def render(self) -> Presentation:
        words_segments = self.engine.current_run_state()
        words: List[str] = []

        for word_segments in words_segments:
            current_word = ""
            for segment in word_segments:
                match segment.segment_type:
                    case SegmentType.CORRECT:
                        current_word += segment.text
                    case SegmentType.INCORRECT:
                        current_word += color(segment.text, Color.RED)
                    case SegmentType.TO_BE_TYPED:
                        current_word += color(segment.text, Color.BRIGHT_BLACK)
                    case SegmentType.MISSED:
                        current_word += color(segment.text, Color.CYAN)
            words.append(current_word)

        as_string = " ".join(words)

        text_lines = self.chunk_words(as_string, 50)
        prepend = []

        if self.engine.is_run_in_play:
            prepend.append("")
        elif self.engine.current_run is not None and not self.engine.is_run_started:
            prepend.append("Type a letter to start!")

        return Presentation(
            width=self.settings.width,
            height=self.settings.height,
            top_bar=Bar(elements=["[ESC] Return to menu", "[TAB] restart run" ], width=round(self.settings.width / 2)),
            slide=Slide.CENTERED_XY(lines=prepend + text_lines)
        )

    def chunk_words(self, text: str, size: int) -> List[str]:
        text = text.strip()
        if not text:
            return []

        words = text.split()
        lines: List[str] = []
        current_line = ""

        for word in words:
            if not current_line:
                current_line = word
            elif visible_len(current_line) + 1 + visible_len(word) <= size:
                current_line += " " + word
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines
    
    @override
    def handle_input(self, input_event: InputEvent):
        match input_event.type:
            case IET.CHAR:
                self.engine.type_char(input_event.char)
            case IET.ESCAPE:
                self.is_to_return = True
            case IET.BACKSPACE:
                self.engine.backspace()
            case IET.TAB:
                self.engine.new_run(self.word_count)
            case _:
                pass

    @override
    def next_screen(self) -> Optional[Screen]:
        if self.is_to_return:
            self.is_to_return = False
            return self.return_to()
        return self.__next_screen

    @override
    def return_to(self) -> Optional[Screen]:
        return self.__return_to


