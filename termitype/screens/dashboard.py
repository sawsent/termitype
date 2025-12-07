from termitype.adapters.base import Adapter
from termitype.app.context import AppContext
from termitype.models.engine.runreport import RunReport
from termitype.models.inputevent import InputEvent, InputEventType as IET
from termitype.models.presentation.presentation import Bar, Line, LineStyle, Presentation, Slide
from termitype.screens.base import Screen
from typing import  List, Optional, override, Self

from termitype.utils.visuals import TOP_BAR_MENU

class DashboardScreen(Screen):

    def __init__(self, context: AppContext):
        self.context = context
        self.adapter: Adapter = context.adapter

    @property
    def runs(self) -> List[RunReport]:
        return self.context.runs

    @override
    def restart(self) -> Self:
        self.__next_screen: Optional[Screen] = self
        self.total_runs = len(self.runs)
        self.valid_runs = [r for r in self.runs if r.accuracy > 85]
        self.valid_runs_amount = len(self.valid_runs)
        if len(self.context.runs) == 0:
            self.most_recent_run = None 
        else:
            self.most_recent_run = max(self.runs, key=lambda r: r.start_time)

        self.wpm_values = [r.wpm for r in self.valid_runs]
        self.acc_values = [r.accuracy for r in self.valid_runs]

        if len(self.wpm_values) == 0:
            self.personal_best_wpm = 0
            self.average_wpm = 0
            self.best_accuracy = 0
            self.average_accuracy = 0
        else:
            self.personal_best_wpm = max(self.wpm_values)
            self.average_wpm = sum(self.wpm_values) / len(self.wpm_values)
            self.best_accuracy = max(self.acc_values)
            self.average_accuracy = sum(self.acc_values) / len(self.acc_values)

        self.lines = [
            ["personal best", str(round(self.personal_best_wpm, 2))],
            ["avg wpm", str(round(self.average_wpm, 2))],
            ["avg accuracy", str(round(self.average_accuracy, 2))],
            ["valid runs", str(self.valid_runs_amount)],
            ["total runs", str(self.total_runs)],
        ]
        return self

    def render(self) -> Presentation:
        slide = Slide.CENTERED(
            lines=[Line.CENTER(e, padding=10, outlined=True) for e in self.lines]
        )
        return self.get_presentation(slide)

    def get_presentation(self, slide: Slide) -> Presentation:
        return Presentation(
            slide=slide,
            width=self.context.settings.width,
            height=self.context.settings.height,
            top_bar=TOP_BAR_MENU if self.context.settings.show_logo else Bar.EMPTY(),
            bottom_bar=Bar.SINGLE(["[ESC] settings", "[TAB] run"], style=LineStyle.ALIGNED_RIGHT(gap=4, padding_right=2)),
            show_outline=self.context.settings.display_outline

        )
    
    def handle_input(self, input_event: InputEvent):
        match input_event.type:
            case IET.ESCAPE:
                self.__next_screen = self.context.settings_screen.restart()
            case IET.TAB:
                self.__next_screen = self.context.run_screen.restart()

    def next_screen(self) -> Optional[Screen]:
        return self.__next_screen

