from termitype.adapters.base import Adapter
from termitype.views.base import View

class AppConfig:
    def __init__(self, adapter: Adapter, first_view: View):
        self.adapter = adapter
        self.starting_view = first_view

