from termitype.adapters.base import Adapter
from termitype.models.inputevent import InputEvent, InputEventType as IET
from termitype.models.presentation.presentation import Presentation, Line, Slide
from termitype.models.settings import DisplaySettings
from termitype.screens.base import Screen
from typing import Optional, override, Self

class SettingsScreen(Screen):

    def __init__(self, adapter: Adapter, menu: Screen, settings: DisplaySettings):
        super().__init__(settings)
        self.adapter: Adapter = adapter
        self.__return_to: Screen = menu
        self.restart()
        
    @override
    def restart(self) -> Self:
        self.last_key_press: str = ""
        self.is_to_return: bool = False
        self.__next_screen: Optional[Screen] = self
        return self

    def render(self) -> Presentation:
        return Presentation(slide=Slide.CENTERED_XY(["This is the settings view [Esc] to go back"]), width=self.settings.width, height=self.settings.height)

    def handle_input(self, input_event: InputEvent):
        match input_event.type:
            case IET.ESCAPE:
                self.is_to_return = True
            case IET.CHAR: 
                self.last_key_press = input_event.char
            case _:
                pass

    def next_screen(self) -> Optional[Screen]:
        if self.is_to_return:
            self.is_to_return = False
            return self.return_to()
        return self.__next_screen
    
    def return_to(self) -> Optional[Screen]:
        return self.__return_to

