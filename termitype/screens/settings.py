from termitype.adapters.base import Adapter
from termitype.app.context import AppContext
from termitype.models.inputevent import InputEvent, InputEventType as IET
from termitype.models.presentation.presentation import Bar, BarStyle, Presentation, Line, Slide
from termitype.models.settings import DisplaySettings
from termitype.screens.base import Screen
from typing import Optional, override, Self

from termitype.utils.topbar import TOP_BAR_MENU

class SettingsScreen(Screen):

    def __init__(self, context: AppContext):
        self.context = context
        self.adapter: Adapter = context.adapter
        self.menu: Screen = context.menu_screen
        self.run_screen: Screen = context.run_screen
        self.restart()

    @property
    def settings(self):
        return self.context.settings
        
    @override
    def restart(self) -> Self:
        self.last_key_press: str = ""
        self.is_to_return: bool = False
        self.__next_screen: Optional[Screen] = self
        return self

    def render(self) -> Presentation:
        return Presentation(
            slide=Slide.CENTERED_XY(["This is the settings view"]),
            width=self.settings.width,
            height=self.settings.height,
            top_bar=TOP_BAR_MENU,
            bottom_bar=Bar.SINGLE(["[ESC] menu", "[TAB] run"], style=BarStyle.ALIGNED_RIGHT(gap=5, padding_right=2))
        )

    def handle_input(self, input_event: InputEvent):
        match input_event.type:
            case IET.ESCAPE:
                self.__next_screen = self.menu
            case IET.TAB:
                self.__next_screen = self.run_screen
            case IET.CHAR: 
                self.last_key_press = input_event.char
                match input_event.char:
                    case "w": self.context.update_settings(width=self.context.settings.width + 1)
                    case "W": self.context.update_settings(width=self.context.settings.width - 1)
            case _:
                pass

    def next_screen(self) -> Optional[Screen]:
        return self.__next_screen
    
    def return_to(self) -> Optional[Screen]:
        return self.menu

