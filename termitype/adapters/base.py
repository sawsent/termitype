from abc import ABC, abstractmethod

class Adapter(ABC):
    """
    Abstract base class for terminal adapters.
    Handles input and output for different platforms.
    """

    @abstractmethod
    def startup(self) -> None:
        """
        Startup for the adapter (hide cursor, ...)
        """
        pass

    @abstractmethod
    def render(self, text: str):
        """
        Render text to the terminal.
        Could handle color, formatting, etc.

        :param text: The string to display
        """
        pass

    @abstractmethod
    def get_key(self) -> str:
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

