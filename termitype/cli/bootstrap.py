from termitype.app.app import App
from termitype.adapters.macos import MacAdapter
from termitype.cli.shutdown import shutdown
from termitype.core.engine import TypingEngine
from termitype.screens.typingrun import TypingRunScreen
from termitype.screens.settings import SettingsScreen
from termitype.app.context import context

from termitype.storage.storagemanager import StorageManager

def main():
    adapter = MacAdapter()
    storage_manager = StorageManager()
    context.storage_manager = storage_manager

    context.settings = storage_manager.load_settings()
    context.language = storage_manager.load_language(context.settings.language)
    context.adapter = adapter

    settings_screen = SettingsScreen(context)
    context.settings_screen = settings_screen

    engine = TypingEngine(context)
    typing_run_screen = TypingRunScreen(context, engine)
    context.run_screen = typing_run_screen

    app = App(adapter, typing_run_screen)

    try:
        adapter.startup()
        app.run()
    finally:
        adapter.finalize()
        context.save_settings()

    shutdown(context)

