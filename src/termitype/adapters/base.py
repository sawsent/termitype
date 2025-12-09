from abc import ABC, abstractmethod
from typing import Tuple

from termitype.models.inputevent import InputEvent
from termitype.models.presentation.presentation import Presentation

class Adapter(ABC):
    """
    Abstract base class for terminal adapters.
    Handles input and output for different platforms.
    """

    @abstractmethod
    def get_terminal_size(self) -> Tuple[int, int]:
        """
        Gets the size of the terminal (width, height)
        """
        pass

    @abstractmethod
    def startup(self) -> None:
        """
        Startup for the adapter (hide cursor, ...)
        """
        pass

    @abstractmethod
    def render(self, presentation: Presentation):
        """
        Render text to the terminal.
        Could handle color, formatting, etc.

        :param text: The string to display
        """
        pass

    @abstractmethod
    def get_input_event(self) -> InputEvent:
        """
        Read a single keypress from the user.

        :return: The key pressed as a string
        """
        pass

    @abstractmethod
    def clear(self):
        """
        Clear the terminal screen (or the relevant region).
        """
        pass

    @abstractmethod
    def finalize(self):
        """
        Clean up terminal state when exiting.
        For example, restore cursor visibility or colors.
        """
        pass

