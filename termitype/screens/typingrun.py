from termitype.app.app import App
from termitype.app.context import AppContext
from termitype.core.engine import TypingEngine
from termitype.models.engine.run import Run, RunSegment, SegmentType
from termitype.models.inputevent import InputEvent, InputEventType as IET
from termitype.models.presentation.presentation import Bar, BarStyle, Presentation, Line, Slide
from termitype.models.settings import DisplaySettings, Settings, TypingRunSettings
from termitype.screens.base import Screen
from termitype.adapters.base import Adapter
from typing import Optional, override, List, Self

from termitype.utils.color import Color, color, visible_len
from termitype.utils.topbar import TOP_BAR_MENU

class TypingRunScreen(Screen):
    BOT_BAR = Bar.SINGLE(["[ESC] settings", "[TAB] restart" ], style=BarStyle.ALIGNED_RIGHT(padding_right=2, gap=5))

    def __init__(self, context: AppContext, typing_engine: TypingEngine):
        self.context = context
        self.adapter: Adapter = context.adapter
        self.__return_to: Screen = context.menu_screen
        self.engine = typing_engine
        self.restart()

    @property
    def run_settings(self) -> TypingRunSettings:
        return TypingRunSettings.from_settings(self.settings)

    @property
    def settings(self) -> Settings:
        return self.context.settings

    @override
    def restart(self) -> Self:
        self.last_key_press: str = ""
        self.is_to_return: bool = False
        self.__next_screen: Optional[Screen] = self
        self.engine.new_run(self.run_settings)
        return self

    def get_presentation(self, slide: Slide) -> Presentation:
        return Presentation(
            width=self.settings.width,
            height=self.settings.height,
            top_bar=TOP_BAR_MENU,
            bottom_bar=self.BOT_BAR,
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
        text_lines = self.chunk_words(self.colored_run_segments(run.get_segments()), self.run_settings.test_text_max_width)

        return self.get_presentation(
            Slide.CENTERED_XY(lines=[""] + text_lines)
        )

    def render_unstarted_run(self, run: Run) -> Presentation:
        text_lines = self.chunk_words(self.colored_run_segments(run.get_segments()), self.run_settings.test_text_max_width)

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


