from typing import Optional
from termitype.screens.base import Screen
from termitype.adapters.base import Adapter
from termitype.storage.storagemanager import StorageManager


class App:
    def __init__(self, adapter: Adapter, starting_view: Screen):
        self.adapter = adapter
        self.screen: Optional[Screen] = starting_view


    def run(self):
        while self.screen is not None:
            presentation = self.screen.render()
            self.adapter.render(presentation)

            input_event = self.adapter.get_input_event()
            self.screen.handle_input(input_event)

            self.screen = self.screen.next_screen()

