from termitype.adapters.base import Adapter
from termitype.app.context import AppContext
from termitype.models.inputevent import InputEvent, InputEventType as IET
from termitype.models.presentation.presentation import Bar, LineStyle, Presentation, Slide
from termitype.screens.base import Screen
from typing import Optional, override, Self

from termitype.utils.visuals import TOP_BAR_MENU

class SettingsScreen(Screen):

    def __init__(self, context: AppContext):
        self.context = context
        self.adapter: Adapter = context.adapter
        self.restart()

    @override
    def restart(self) -> Self:
        self.__next_screen: Optional[Screen] = self
        return self

    def render(self) -> Presentation:
        return Presentation(
            slide=Slide.CENTERED_XY(["This is the settings view"]),
            width=self.context.settings.width,
            height=self.context.settings.height,
            top_bar=TOP_BAR_MENU,
            bottom_bar=Bar.SINGLE(["[q] quit", "[TAB] run"], style=LineStyle.ALIGNED_RIGHT(gap=5, padding_right=2)),
            show_outline=self.context.settings.display_outline
        )

    def handle_input(self, input_event: InputEvent):
        match input_event.type:
            case IET.ESCAPE:
                self.__next_screen = None
            case IET.TAB:
                self.__next_screen = self.context.run_screen
            case IET.CHAR: 
                match input_event.char:
                    case "q": self.__next_screen = None
                    case "w": self.context.update_settings(width=self.context.settings.width + 1)
                    case "W": self.context.update_settings(width=self.context.settings.width - 1)
            case _:
                pass

    def next_screen(self) -> Optional[Screen]:
        next = self.__next_screen
        if self.__next_screen is not self:
            self.restart()
        return next

