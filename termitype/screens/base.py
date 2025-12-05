from abc import ABC, abstractmethod
from typing import Self, Optional
from termitype.models.inputevent import InputEvent
from termitype.models.presentation.presentation import Presentation

class Screen(ABC):
    """
    Abstract base class for all Views in Termitype.
    Each view must implement rendering, input handling, and next state logic.
    """
    @abstractmethod
    def restart(self) -> Self:
        """
        Clears internal state.
        """
        pass

    @abstractmethod
    def render(self) -> Presentation:
        """
        Create the presentation with the given size.
        """
        pass

    @abstractmethod
    def handle_input(self, input_event: InputEvent):
        """
        Handle a single keypress or command.

        :param key: The input from the user
        """
        pass

    @abstractmethod
    def next_screen(self) -> Optional[Self]:
        """
        Determine what the next view/state should be.

        :return: Another BaseView instance or None (to quit)
        """
        pass
