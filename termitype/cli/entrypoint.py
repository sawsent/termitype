from termitype.app.app import App
from termitype.app.config import AppConfig
from termitype.adapters.dummy import DummyAdapter
from termitype.views.dummy import DummyView
from termitype.views.menu import MenuView
from termitype.views.settings import SettingsView

def main():
    adapter = DummyAdapter()
    menu = MenuView(adapter)
    menu.register_view(id="r", view=DummyView(adapter, menu), description="Run test!")
    menu.register_view(id="s", view=SettingsView(adapter, menu), description="Settings")
    menu.register_view(id="q", view=None, description="Quit")

    config = AppConfig(adapter, menu)
    app = App(config)

    app.run()


