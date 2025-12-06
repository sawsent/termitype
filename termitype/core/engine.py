from typing import List, Optional
import random

from termitype.app.context import AppContext
from termitype.models.engine.run import Run


class TypingEngine:
    def __init__(self, context: AppContext) -> None:
        self.context = context
        self.current_run: Optional[Run] = None

    @property
    def language(self) -> List[str]:
        return self.context.language

    def new_run(self, word_amount: int):
        words = random.choices(self.language, k=word_amount)
        self.current_run = Run(words)

    def type_char(self, char: str) -> None:
        if self.current_run is not None and not self.current_run.started:
            self.current_run.start()

        if self.current_run is not None and self.current_run.in_play:
            self.current_run.type_char(char)
            if self.current_run.should_auto_finish():
                self.current_run.auto_finish_prep()
            if self.current_run.should_finish():
                self.end_run()

    def backspace(self) -> None:
        if self.current_run is not None and self.current_run.in_play:
            self.current_run.backspace()
        
    def start_run(self):
        if self.current_run is not None:
            self.current_run.start()

    def end_run(self):
        if self.current_run is not None:
            self.current_run.finish()
            report = self.current_run.get_run_report()
            if report is not None:
                self.context.runs.append(report)

    @property
    def is_run_in_play(self) -> bool:
        return self.is_run_started and not self.is_run_finished

    @property
    def is_run_started(self) -> bool:
        if self.current_run is not None:
            return self.current_run.started
        else:
            return False

    @property
    def is_run_finished(self) -> bool:
        if self.current_run is not None:
            return self.current_run.finished
        else:
            return False

    def current_run_state(self) -> Optional[Run]:
        return self.current_run


