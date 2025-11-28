from termitype.adapters.base import Adapter
from termitype.views.base import View
from typing import Optional, Dict, Self

class SettingsView(View):

    def __init__(self, adapter: Adapter, menu: View):
        self.last_key_press: str = ""
        self.adapter: Adapter = adapter
        self.menu = menu
        self.__next_view: Optional[View] = self

    def render(self):
        self.adapter.render("This is the settings view, press q to go back to menu")

    def handle_input(self, key):
        self.last_key_press = key
        match key:
            case "q": self.__next_view = self.return_to()
            case _: self.__next_view = self

    def next_view(self) -> Optional[View]:
        return self.__next_view
    
    def return_to(self) -> Optional[View]:
        return self.menu

