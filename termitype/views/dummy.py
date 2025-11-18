from termitype.views.base import View
from termitype.adapters.base import Adapter
from typing import Optional, override

class DummyView(View):

    def __init__(self, adapter: Adapter, menu: View):
        self.adapter: Adapter = adapter
        self.last_key_press: str = ""
        self.menu_view: View = menu
        self.__next_view: Optional[View] = self

    @override
    def render(self):
        self.adapter.render(f"Last key pressed: {self.last_key_press}, [q] to go back to menu.")

    @override
    def handle_input(self, key: str):
        self.last_key_press: str = key

        match key:
            case "q": self.__next_view = self.return_to()
            case _: self.__next_view = self

    @override
    def next_view(self) -> Optional[View]:
        return self.__next_view

    @override
    def return_to(self) -> Optional[View]:
        return self.menu_view

    
