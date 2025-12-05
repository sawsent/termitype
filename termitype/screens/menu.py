from termitype.app.context import AppContext
from termitype.models.inputevent import InputEvent, InputEventType as IET
from termitype.models.presentation.presentation import Presentation, Line, Slide
from termitype.screens.base import Screen
from typing import Optional, Dict, Self, override
from termitype.models.settings import DisplaySettings, Settings
from termitype.utils.topbar import TOP_BAR_MENU

class MenuScreen(Screen):

    def __init__(self, context: AppContext):
        self.context = context
        self.screens: Dict[str, Screen] = {}
        self.screen_descriptions: Dict[str, str] = {}
        self.__next_screen: Optional[Screen] = self
        self.is_to_return: bool = False

    def register_screen(self, id: str, view: Screen, description: str) -> Self:
        self.screens[id] = view
        self.screen_descriptions[id] = description
        return self

    @property
    def settings(self) -> Settings:
        return self.context.settings

    @override
    def render(self) -> Presentation:
        welcome = [
            "Welcome to termitype!",
            "[ESC] Quit"
        ]
        lines = [f"[{k}] {v}" for k, v in self.screen_descriptions.items()]
        slide = Slide.CENTERED_XY(welcome + lines)
        return Presentation(slide=slide, width=self.settings.width, height=self.settings.height, top_bar=TOP_BAR_MENU)

    @override
    def handle_input(self, input_event: InputEvent):
        match input_event.type:
            case IET.CHAR:
                self.__next_screen = self.screens.get(input_event.char, self).restart()
            case IET.ESCAPE:
                self.is_to_return = True
            case _:
                pass

    @override
    def next_screen(self) -> Optional[Screen]:
        if self.is_to_return:
            return self.return_to()
        return self.__next_screen

    @override
    def return_to(self) -> Optional[Screen]:
        return None

    @override
    def restart(self) -> Self:
        return self

