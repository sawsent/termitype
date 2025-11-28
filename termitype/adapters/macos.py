from termitype.adapters.base import Adapter
from typing import List, override

import sys
import os
import termios
import tty

class MacAdapter(Adapter):

    def __init__(self):
        pass

    @override
    def startup(self):
        self.hide_cursor()

    @override
    def render(self, text: str):
        (terminal_lines, terminal_columns) = os.get_terminal_size()

        self.clear()

        lines = text.split("\n")
        x_size = len(max(lines, key=len))
        y_size = len(lines)

        y_indent = round((terminal_columns / 2) - (y_size / 2))
        x_indent = round((terminal_lines / 2) - (x_size / 2))
        
        self.indent_y(y_indent)
        sys.stdout.write(self.indent_x(lines, x_indent))
        sys.stdout.flush()


    def indent_x(self, lines: List[str], indentation: int) -> str:
        return "\n".join(map(lambda line: f"{" " * indentation}{line}", lines))

    def indent_y(self, indentation: int) -> None:
        sys.stdout.write("\n" * indentation)

    @override
    def get_key(self) -> str:
        """
        Reads a single keypress using raw terminal mode.
        Blocks until a key is pressed.
        """
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            tty.setraw(fd)
            char = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        return char

    @override
    def clear(self) -> None:
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()

    @override
    def finalize(self):
        self.show_cursor()
        self.clear()

    def show_cursor(self):
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

    def hide_cursor(self):
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()


