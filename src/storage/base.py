from abc import ABC, abstractmethod
from typing import Any, List, Dict

class Storage(ABC):
    """
    Abstract base class for storage backends.
    Defines how run data is saved and retrieved.
    """

    @abstractmethod
    def save_run(self, run_data: Dict[str, Any]):
        """
        Save a typing run.

        :param run_data: Dictionary containing run info (WPM, accuracy, words, timestamp, etc.)
        """
        pass

    @abstractmethod
    def get_all_runs(self) -> List[Dict[str, Any]]:
        """
        Retrieve all stored runs.

        :return: List of run dictionaries
        """
        pass

    @abstractmethod
    def clear_runs(self):
        """
        Delete all stored runs.
        """
        pass

