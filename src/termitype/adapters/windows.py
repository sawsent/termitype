from termitype.adapters.base import Adapter
from typing import override, Tuple
import sys
import os
import msvcrt
import ctypes

from termitype.models.inputevent import InputEvent
from termitype.models.presentation.cursor import Cursor, CursorStyle
from termitype.models.presentation.presentation import Presentation


class WindowsAdapter(Adapter):

    def __init__(self):
        self._enable_ansi()

    @override
    def get_terminal_size(self) -> Tuple[int, int]:
        return os.get_terminal_size()

    @override
    def startup(self):
        self.hide_cursor()

    @override
    def render(self, presentation: Presentation):
        terminal_width, terminal_height = os.get_terminal_size()

        self.clear()

        y_indent = round((terminal_height - presentation.height) / 2)
        x_indent = round((terminal_width - presentation.width) / 2)

        self.indent_y(y_indent)
        sys.stdout.write(self.indent_x(presentation.as_text(), x_indent))
        sys.stdout.flush()
        self.draw_cursor(presentation.cursor)

    def draw_cursor(self, cursor: Cursor):
        sys.stdout.write(
            f"\x1b[{cursor.line};{cursor.col}H{CursorStyle.get_repr(cursor.style)}"
        )
        sys.stdout.flush()

    def indent_x(self, text: str, indentation: int) -> str:
        return "\n".join(
            [f"{' ' * indentation}{line}" for line in text.split("\n")]
        )

    def indent_y(self, indentation: int) -> None:
        sys.stdout.write("\n" * indentation)

    @override
    def get_input_event(self) -> InputEvent:
        """
        Reads a single keypress on Windows.
        Blocks until a key is pressed.
        """
        char = msvcrt.getwch()

        match char:
            case "\x1b":
                return InputEvent.ESCAPE()
            case "\t":
                return InputEvent.TAB()
            case "\r":
                return InputEvent.ENTER()
            case "\b":
                return InputEvent.BACKSPACE()
            case _ if len(char) == 1 and char.isprintable():
                return InputEvent.CHAR(char)

        return InputEvent.EMPTY()

    @override
    def clear(self) -> None:
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()

    @override
    def finalize(self):
        self.clear()
        self.show_cursor()

    def show_cursor(self):
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

    def hide_cursor(self):
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

    def _enable_ansi(self):
        """
        Enables ANSI escape code support on Windows terminals.
        Required for cursor movement, colors, etc.
        """
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
        mode = ctypes.c_uint32()
        kernel32.GetConsoleMode(handle, ctypes.byref(mode))
        kernel32.SetConsoleMode(handle, mode.value | 0x0004)

