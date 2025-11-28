from typing import Optional
from termitype.app.config import AppConfig
from termitype.views.base import View

class App:

    def __init__(self, config: AppConfig):
        self.adapter = config.adapter
        self.view: Optional[View] = config.starting_view
        self.previous_view: Optional[View] = None

    def run(self):
        while self.view is not None:
            self.view.render()

            key = self.adapter.get_key()
            self.view.handle_input(key)

            self.view = self.view.next_view()

