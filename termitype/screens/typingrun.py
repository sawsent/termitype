from termitype.core.engine import TypingEngine
from termitype.models.engine.run import Run, RunSegment, SegmentType
from termitype.models.inputevent import InputEvent, InputEventType as IET
from termitype.models.presentation.presentation import Bar, Presentation, Line, Slide
from termitype.models.settings import DisplaySettings, Settings, TypingRunSettings
from termitype.screens.base import Screen
from termitype.adapters.base import Adapter
from typing import Optional, override, List, Self

from termitype.utils.color import Color, color, visible_len

class TypingRunScreen(Screen):

    def __init__(self, adapter: Adapter, menu: Screen, typing_engine: TypingEngine, settings: Settings):
        super().__init__(DisplaySettings.from_settings(settings))
        self.run_settings = TypingRunSettings.from_settings(settings)
        self.adapter: Adapter = adapter
        self.__return_to: Screen = menu
        self.engine = typing_engine
        self.TOP_BAR = Bar(elements=["[ESC] Return to menu", "[TAB] restart run" ], width=round(self.settings.width))
        self.restart()

    @override
    def restart(self) -> Self:
        self.last_key_press: str = ""
        self.is_to_return: bool = False
        self.__next_screen: Optional[Screen] = self
        self.engine.new_run(self.run_settings)
        return self

    def get_presentation(self, slide: Slide, top_bar: Optional[Bar] = None, width: Optional[int] = None, height: Optional[int] = None) -> Presentation:
        _top_bar = top_bar if top_bar is not None else self.TOP_BAR
        _width = width if width is not None else self.settings.width
        _height = height if height is not None else self.settings.height

        return Presentation(
            width=_width,
            height=_height,
            top_bar=_top_bar,
            slide=slide
        )


    @override
    def render(self) -> Presentation:
        run = self.engine.current_run_state()

        if run is not None and run.in_play:
            return self.render_in_play_run(run)
        elif run is not None and not run.started:
            return self.render_unstarted_run(run)
        elif run is not None and run.finished:
            return self.render_finished_run(run)

        return self.get_presentation(Slide.CENTERED_XY(lines=["something went wrong"]))



    def render_in_play_run(self, run: Run) -> Presentation:
        text_lines = self.chunk_words(self.colored_run_segments(run.get_segments()), self.settings.width)

        return self.get_presentation(
            Slide.CENTERED_XY(lines=[""] + text_lines)
        )

    def render_unstarted_run(self, run: Run) -> Presentation:
        text_lines = self.chunk_words(self.colored_run_segments(run.get_segments()), self.settings.width)

        return self.get_presentation(
            Slide.CENTERED_XY(lines=["Type any letter to start!"] + text_lines)
        )

    def render_finished_run(self, run: Run) -> Presentation:
        report = run.get_run_report()
        if report is not None:
            return self.get_presentation(
                slide=Slide.CENTERED_XY(lines=[
                    f"time: {round(report.time_s, 2)}, wpm: {report.wpm}, accuracy: {report.accuracy}%",
                    "",
                    "[s] save run"
                ])
            )
        else:
            return self.get_presentation(slide=Slide.CENTERED_XY(lines=["something went wrong when generating the report"]))

    def colored_run_segments(self, segments: List[RunSegment]) -> str:
        as_text: str = ""

        for seg in segments:
            match seg.segment_type:
                case SegmentType.CORRECT:
                    as_text += color(seg.text, Color.BRIGHT_WHITE)
                case SegmentType.INCORRECT:
                    as_text += color(seg.text, Color.RED)
                case SegmentType.TO_BE_TYPED:
                    as_text += color(seg.text, Color.BRIGHT_BLACK)
                case SegmentType.MISSED:
                    as_text += color(seg.text, Color.CYAN)

        return as_text


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
            case IET.CHAR if not self.engine.is_run_finished:
                self.engine.type_char(input_event.char)
            case IET.CHAR if self.engine.is_run_finished:
                match input_event.char:
                    case "s":
                        "save run"
                    case _:
                        pass
            case IET.ESCAPE:
                self.is_to_return = True
            case IET.BACKSPACE:
                self.engine.backspace()
            case IET.TAB:
                self.engine.new_run(self.run_settings)
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


