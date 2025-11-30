from termitype.app.app import App
from termitype.adapters.macos import MacAdapter
from termitype.screens.sandbox import SandboxScreen
from termitype.screens.typingrun import TypingRunScreen
from termitype.screens.menu import MenuScreen
from termitype.screens.settings import SettingsScreen
from termitype.storage.settings import default_settings
from termitype.models.settings import DisplaySettings
from pathlib import Path

def main():
    adapter = MacAdapter()

    settings = default_settings()
    display_settings = DisplaySettings.from_settings(settings)

    menu = MenuScreen(display_settings)
    menu.register_screen(id="r", view=TypingRunScreen(adapter, menu, display_settings), description="Run test!")
    menu.register_screen(id="s", view=SettingsScreen(adapter, menu, display_settings), description="Settings")
    menu.register_screen(id="b", view=SandboxScreen(adapter, menu, display_settings), description="Sandbox")

    app = App(adapter, menu)

    try:
        adapter.startup()
        app.run()
    finally:
        adapter.finalize()


