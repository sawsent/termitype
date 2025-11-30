from termitype.models.inputevent import InputEvent, InputEventType as IET
from termitype.models.presentation.presentation import Presentation
from termitype.models.settings import DisplaySettings
from termitype.screens.base import Screen
from termitype.adapters.base import Adapter
from typing import Optional, override, List, Self

class SandboxScreen(Screen):

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
        text_lines = self.chunk_words(self.text, 50)
        return Presentation(
            lines=[
                "SANDBOX: TYPE AWAY ([ESC] to go back to menu, [TAB] to clear text)"
            ] + text_lines
        )

    def chunk_words(self, text: str, size: int) -> List[str]:
        if text.strip() == "":
            return []
        remaining_text: str = text
        lines = []
        while remaining_text is not "":
            current_line = "" 
            while True:
                next_word = remaining_text.split(" ")[0]
                if len((current_line + " " + next_word).strip()) > size or remaining_text.strip() == "":
                    break
                current_line = f"{current_line} {next_word}"
                remaining_text = " ".join(remaining_text.split(" ")[1:]).strip()
            lines += [current_line]

        cursor = "|"
        if text.endswith(" "):
            cursor = " |"

        last_line = lines[-1] + cursor
        lines.pop()

        return lines + [last_line]



    @override
    def handle_input(self, input_event: InputEvent):
        match input_event.type:
            case IET.CHAR:
                self.last_key_press = input_event.char
                self.text += input_event.char
            case IET.ESCAPE:
                self.is_to_return = True
            case IET.TAB:
                self.text = ""
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


