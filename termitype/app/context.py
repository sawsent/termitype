
from typing import List, Optional
from termitype.adapters.base import Adapter
from termitype.models.settings import Settings
from termitype.screens.base import Screen
from termitype.storage.storagemanager import StorageManager


class AppContext:
    adapter: Adapter
    settings: Settings
    storage_manager: StorageManager
    settings_screen: Screen
    run_screen: Screen
    language: List[str]

    def set_run_screen(self, run_screen: Screen) -> None:
        self.run_screen = run_screen

    def update_settings(self, width: Optional[int] = None) -> None:
        self.settings = Settings(
            width = width if width is not None else self.settings.width
        )

    def update_language(self, language: str) -> None:
        lang = self.storage_manager.load_language(language)
        if not lang:
            return
        else:
            self.language = lang



    def save_settings(self) -> None:
        self.storage_manager.save_settings(self.settings)

context = AppContext()


