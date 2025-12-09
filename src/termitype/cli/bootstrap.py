from termitype.app.app import App
from termitype.cli.shutdown import shutdown
from termitype.core.engine import TypingEngine
from termitype.screens.dashboard import DashboardScreen
from termitype.screens.typingrun import TypingRunScreen
from termitype.screens.settings import SettingsScreen
from termitype.app.context import context

from termitype.storage.storagemanager import StorageManager

import sys
import platform

def bootstrap():

    adapter = get_adapter()

    storage_manager = StorageManager()
    context.storage_manager = storage_manager

    context.settings = storage_manager.load_settings()
    context.language = storage_manager.load_language(context.settings.language)
    context.adapter = adapter

    settings_screen = SettingsScreen(context)
    context.settings_screen = settings_screen

    dashboard_screen = DashboardScreen(context)
    context.dashboard_screen = dashboard_screen

    engine = TypingEngine(context)
    typing_run_screen = TypingRunScreen(context, engine)
    context.run_screen = typing_run_screen

    context.load_runs()

    context.start_screens()

    app = App(adapter, typing_run_screen)

    try:
        adapter.startup()
        app.run()
    finally:
        adapter.finalize()
        context.save_settings()

    shutdown(context)

def get_adapter():
    system = platform.system()

    match platform.system():
        case "Darwin":
            from termitype.adapters.macos import MacAdapter
            return MacAdapter()
        case "Linux":
            sys.exit("Error: Linux adapter is not yet implemented. Termitype currently supports macOS only.")
        case "Windows":
            sys.exit("Error: Windows adapter is not yet implemented. Termitype currently supports macOS only.")
        case _:
            sys.exit(f"Error: Unsupported OS '{system}'. Termitype currently supports macOS only.")

