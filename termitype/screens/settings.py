from termitype.adapters.base import Adapter
from termitype.models.inputevent import InputEvent, InputEventType as IET
from termitype.models.presentation.presentation import Bar, BarStyle, Presentation, Line, Slide
from termitype.models.settings import DisplaySettings
from termitype.screens.base import Screen
from typing import Optional, override, Self

from termitype.utils.topbar import TOP_BAR_MENU

class SettingsScreen(Screen):

    def __init__(self, adapter: Adapter, menu: Screen, run_screen: Screen, settings: DisplaySettings):
        super().__init__(settings)
        self.adapter: Adapter = adapter
        self.menu: Screen = menu
        self.run_screen: Screen = run_screen
        self.restart()
        
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
            case _:
                pass

    def next_screen(self) -> Optional[Screen]:
        return self.__next_screen
    
    def return_to(self) -> Optional[Screen]:
        return self.menu

