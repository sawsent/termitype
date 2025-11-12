from views.base import View
from adapters.base import Adapter
from typing import Self

class DummyView(View):

    def __init__(self, adapter: Adapter):
        self.adapter: Adapter = adapter
        self.last_key_press: str = ""

    def render(self):
        self.adapter.render(f"Last key pressed: {self.last_key_press}")

    def handle_input(self, key: str):
        self.last_key_press: str = key

    def next_view(self) -> Self:
        return self

    
