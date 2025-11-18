from termitype.adapters.base import Adapter
from termitype.views.base import View
from typing import Optional, Dict, Self

class MenuView(View):

    def __init__(self, adapter: Adapter):
        self.last_key_press: str = ""
        self.adapter: Adapter = adapter
        self.views: Dict[str, Optional[View]] = {
            "": None
        }
        self.views_descriptions: Dict[str, str] = {}

    def register_view(self, id: str, view: Optional[View], description: str) -> Self:
        self.views[id] = view
        self.views_descriptions[id] = description
        return self

    def render(self):
        text = "\n".join(f"[{k}] {v}" for k, v in self.views_descriptions.items())
        self.adapter.render(text)

    def handle_input(self, key):
        self.last_key_press = key

    def next_view(self) -> Optional[View]:
        return self.views.get(self.last_key_press)

    def return_to(self) -> Optional[View]:
        return None

