from termitype.app.app import App
from termitype.adapters.macos import MacAdapter
from termitype.core.engine import TypingEngine
from termitype.screens.sandbox import SandboxScreen
from termitype.screens.typingrun import TypingRunScreen
from termitype.screens.menu import MenuScreen
from termitype.screens.settings import SettingsScreen
from termitype.app.context import context
from typing import List

from termitype.storage.storagemanager import StorageManager

def main():
    adapter = MacAdapter()
    storage_manager = StorageManager()
    context.storage_manager = storage_manager

    context.settings = storage_manager.load_settings()
    context.language = storage_manager.load_language(context.settings.language)
    menu = MenuScreen(context)
    context.adapter = adapter
    context.menu_screen = menu

    engine = TypingEngine(context)
    typing_run_screen = TypingRunScreen(context, engine)
    context.run_screen = typing_run_screen


    menu.register_screen(id="r", view=typing_run_screen, description="Back to test")
    menu.register_screen(id="s", view=SettingsScreen(context), description="Settings")
    menu.register_screen(id="b", view=SandboxScreen(context), description="Sandbox")

    app = App(adapter, typing_run_screen)


    try:
        adapter.startup()
        app.run()
    finally:
        context.storage_manager.save_settings(context.settings)
        adapter.finalize()

