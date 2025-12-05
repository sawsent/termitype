
from typing import List, Optional
from termitype.adapters.base import Adapter
from termitype.models.settings import Settings
from termitype.screens.base import Screen
from termitype.storage.storagemanager import StorageManager


class AppContext:
    adapter: Adapter
    settings: Settings
    storage_manager: StorageManager
    menu_screen: Screen
    run_screen: Screen
    language: List[str]

    def update_settings(self, width: Optional[int] = None) -> None:
        self.settings = Settings(
            width = width if width is not None else self.settings.width
        )

context = AppContext()


