from termitype.adapters.base import Adapter
from termitype.app.context import AppContext
from termitype.models.inputevent import InputEvent, InputEventType as IET
from termitype.models.presentation.presentation import Bar, LineStyle, Presentation, Slide
from termitype.screens.base import Screen
from typing import Dict, Optional, override, Self

from termitype.utils.visuals import TOP_BAR_MENU

class SettingsScreen(Screen):

    def __init__(self, context: AppContext):
        self.context = context
        self.adapter: Adapter = context.adapter
        self.restart()

#class Settings():
#    width: int = 100
#    height: int = 30
#    language: str = "english"
#    test_word_count: int = 50
#    test_text_max_width: int = 60
#    test_style: TestStyle = TestStyle.BLOCK
#    ahead: int = 2
#    behind: int = 2
#    show_exit_message: bool = True
#    display_outline: bool = True


    @property
    def v_set(self) -> Dict:
        return {
            "display": {
                "width": {
                    "value": self.context.settings.width,
                    "desc": ""
                },
                "height": {
                    "value": self.context.settings.height,
                    "desc": ""
                },
                "outline": {
                    "value": self.context.settings.display_outline,
                    "desc": ""
                },
            },
            "typing": {
                "language": {
                    "value": self.context.settings.language,
                    "desc": ""
                },
                "words": {
                    "value": self.context.settings.language,
                    "desc": ""
                },
                "style": {
                    "value": self.context.settings.language,
                    "desc": ""
                },
                "ahead": {
                    "value": self.context.settings.language,
                    "desc": ""
                },
                "behind": {
                    "value": self.context.settings.language,
                    "desc": ""
                },
            },
            "general": {
                "exit_message": {
                    "value": self.context.settings.show_exit_message,
                    "desc": ""
                },
            }
        }

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

