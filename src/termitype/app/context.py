from typing import List
from termitype.adapters.base import Adapter
from termitype.models.engine.runreport import RunReport
from termitype.models.settings import Settings
from termitype.screens.base import Screen
from termitype.storage.storagemanager import StorageManager


class AppContext:
    adapter: Adapter
    settings: Settings
    storage_manager: StorageManager
    settings_screen: Screen
    run_screen: Screen
    dashboard_screen: Screen
    language: List[str]
    runs: List[RunReport]

    def save_settings(self) -> None:
        self.storage_manager.save_settings(self.settings)

    def load_runs(self) -> None:
        self.runs = self.storage_manager.load_runs()

    def save_runs(self) -> None:
        self.storage_manager.save_runs(self.runs)

    def start_screens(self) -> None:
        self.settings_screen.restart()
        self.run_screen.restart()
        self.dashboard_screen.restart()

context = AppContext()


