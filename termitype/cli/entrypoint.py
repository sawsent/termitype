from termitype.app.app import App
from termitype.app.config import AppConfig
from termitype.adapters.macos import MacAdapter
from termitype.views.run import RunView
from termitype.views.menu import MenuView
from termitype.views.settings import SettingsView

def main():
    adapter = MacAdapter()
    menu = MenuView(adapter)
    menu.register_view(id="r", view=RunView(adapter, menu), description="Run test!")
    menu.register_view(id="s", view=SettingsView(adapter, menu), description="Settings")
    menu.register_view(id="q", view=None, description="Quit")

    config = AppConfig(adapter, menu)
    app = App(config)

    try:
        adapter.startup()
        app.run()
    finally:
        adapter.finalize()


