from termitype.models.inputevent import InputEvent, InputEventType as IET
from termitype.models.presentation.presentation import Presentation
from termitype.models.settings import DisplaySettings
from termitype.screens.base import Screen
from termitype.adapters.base import Adapter
from typing import Optional, override, List, Self

class TypingRunScreen(Screen):

    def __init__(self, adapter: Adapter, menu: Screen, settings: DisplaySettings):
        super().__init__(settings)
        self.adapter: Adapter = adapter
        self.__return_to: Screen = menu
        self.restart()

    @override
    def restart(self) -> Self:
        self.last_key_press: str = ""
        self.is_to_return: bool = False
        self.text: str = ""
        self.__next_screen: Optional[Screen] = self
        return self


    @override
    def render(self) -> Presentation:
        text_lines = self.chunk(self.text, 50)
        return Presentation(
            lines=[
                "THIS IS THE RUN VIEW",
                f"Last key pressed: {repr(self.last_key_press)}, [Esc] to go back to menu."
            ] + text_lines
        )

    def chunk(self, text: str, size: int) -> List[str]:
        return [text[i:i+size] for i in range(0, len(text), size)]

    @override
    def handle_input(self, input_event: InputEvent):
        match input_event.type:
            case IET.CHAR:
                self.last_key_press = input_event.char
                self.text += input_event.char
            case IET.ESCAPE:
                self.is_to_return = True
            case IET.BACKSPACE:
                self.text = self.text[:-1]
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


