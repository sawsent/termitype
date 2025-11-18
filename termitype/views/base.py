from abc import ABC, abstractmethod
from typing import Self, Optional

class View(ABC):
    """
    Abstract base class for all Views in Termitype.
    Each view must implement rendering, input handling, and next state logic.
    """

    @abstractmethod
    def render(self):
        """
        Draw the view to the terminal via the provided adapter.
        
        :param adapter: The terminal adapter (Linux/mac/PowerShell/etc.)
        """
        pass

    @abstractmethod
    def handle_input(self, key):
        """
        Handle a single keypress or command.

        :param key: The input from the user
        """
        pass

    @abstractmethod
    def next_view(self) -> Optional[Self]:
        """
        Determine what the next view/state should be.

        :return: Another BaseView instance or None (to quit)
        """
        pass

    def return_to(self) -> Optional[Self]:
        """
        Determine what the on-quit view should be

        :return: Another View instance or None (to quit)
        """
        return None

