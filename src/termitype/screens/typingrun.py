from termitype.app.context import AppContext
from termitype.core.engine import TypingEngine
from termitype.models.engine.run import Run, RunSegment, SegmentType
from termitype.models.inputevent import InputEvent, InputEventType as IET
from termitype.models.presentation.presentation import Bar, LineStyle, Presentation, Slide, Line
from termitype.models.settings import Settings
from termitype.screens.base import Screen
from termitype.adapters.base import Adapter
from typing import Optional, override, List, Self

from termitype.utils.color import Color, color, visible_len
from termitype.utils.visuals import TOP_BAR_MENU
from termitype.utils.words import chunk_words

class TypingRunScreen(Screen):
    BOT_BAR = Bar.SINGLE(["[ESC] settings", "[TAB] restart" ], style=LineStyle.ALIGNED_RIGHT(padding_right=2, gap=5))

    def __init__(self, context: AppContext, typing_engine: TypingEngine):
        self.context = context
        self.adapter: Adapter = context.adapter
        self.engine = typing_engine

    @property
    def settings(self) -> Settings:
        return self.context.settings

    @override
    def restart(self) -> Self:
        self.is_to_return: bool = False
        self.__next_screen: Optional[Screen] = self
        self.engine.new_run(self.settings.test_word_count)
        return self

    def get_presentation(self, slide: Slide) -> Presentation:
        return Presentation(
            slide=slide,
            width=self.settings.width,
            height=self.settings.height,
            top_bar=TOP_BAR_MENU if self.settings.show_logo else Bar.EMPTY(),
            bottom_bar=self.BOT_BAR,
            show_outline=self.context.settings.display_outline
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
        text_lines = chunk_words(self.colored_run_segments(run.get_segments()), self.settings.test_text_max_width)

        return self.get_presentation(
            Slide.CENTERED_XY(lines=[""] + text_lines)
        )

    def render_unstarted_run(self, run: Run) -> Presentation:
        text_lines = chunk_words(self.colored_run_segments(run.get_segments()), self.settings.test_text_max_width)

        return self.get_presentation(
            Slide.CENTERED_XY(lines=["Type any letter to start!"] + text_lines)
        )

    def render_finished_run(self, run: Run) -> Presentation:
        report = run.get_run_report()
        if report is not None:
            return self.get_presentation(
                slide=Slide.CENTERED([
                    Line.CENTER([f"WPM: {report.wpm}"], outlined=True),
                    Line.CENTER([f"time: {round(report.time_s, 2)}s, accuracy: {report.accuracy}%"], padding=20),
                ])
            )
        else:
            return self.get_presentation(slide=Slide.CENTERED_XY(lines=["something went wrong when generating the report"]))

    def colored_run_segments(self, segments: List[RunSegment]) -> str:
        as_text: str = ""

        for seg in segments:
            match seg.segment_type:
                case SegmentType.CORRECT:
                    as_text += seg.text # color(seg.text, Color.BRIGHT_WHITE)
                case SegmentType.INCORRECT:
                    as_text += color(seg.text, Color.RED)
                case SegmentType.TO_BE_TYPED:
                    as_text += color(seg.text, Color.BRIGHT_BLACK)
                case SegmentType.MISSED:
                    as_text += color(seg.text, Color.CYAN)

        return as_text

    @override
    def handle_input(self, input_event: InputEvent):
        match input_event.type:
            case IET.CHAR if not self.engine.is_run_finished:
                self.engine.type_char(input_event.char)
            case IET.ESCAPE:
                self.context.save_runs()
                self.__next_screen = self.context.settings_screen.restart()
            case IET.BACKSPACE:
                self.engine.backspace()
            case IET.TAB:
                self.engine.new_run(self.settings.test_word_count)
            case _:
                pass

    @override
    def next_screen(self) -> Optional[Screen]:
        return self.__next_screen


