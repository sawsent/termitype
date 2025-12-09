import json
from pathlib import Path
from typing import List
import importlib.resources as res

from termitype.models.engine.runreport import RunReport
from termitype.models.settings import Settings


try:
    from platformdirs import user_config_dir
except ImportError:
    def user_config_dir(appname): return Path.home() / f".{appname}"

CONFIG_DIR = Path(user_config_dir("termitype"))
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

SETTINGS_PATH = CONFIG_DIR / "settings.json"
RUNS_PATH = CONFIG_DIR / "runs.json"

# Packaged static resources (read-only)
PKG_SETTINGS = "termitype.static"
PKG_LANGUAGES = "termitype.static.languages"


class StorageManager:

    def load_settings(self) -> Settings:
        """
        1. If user settings exist → load them.
        2. Otherwise → load default packaged settings.json.
        3. Save defaults to user config folder for future use.
        """

        if SETTINGS_PATH.exists():
            with SETTINGS_PATH.open("r") as f:
                data = json.load(f)
                return self._parse_settings(data)

        with res.open_text(PKG_SETTINGS, "settings.json") as f:
            default_data = json.load(f)

        with SETTINGS_PATH.open("w") as f:
            json.dump(default_data, f, indent=4)

        return self._parse_settings(default_data)

    def _parse_settings(self, data: dict) -> Settings:
        """Convert JSON dict to Settings model."""
        return Settings(
            width=data["display"]["width"],
            height=data["display"]["height"],
            display_outline=data["display"]["outline"],
            test_word_count=data["typing"]["word_count"],
            test_text_max_width=data["typing"]["line_max_width"],
            language=data["typing"]["language"],
            show_exit_message=data["general"]["show_exit_message"],
            show_logo=data["general"]["show_logo"],
        )

    def save_settings(self, settings: Settings) -> None:
        """Store settings to the user config folder."""
        settings_json = {
            "display": {
                "width": settings.width,
                "height": settings.height,
                "outline": settings.display_outline,
            },
            "typing": {
                "language": settings.language,
                "line_max_width": settings.test_text_max_width,
                "word_count": settings.test_word_count,
            },
            "general": {
                "show_exit_message": settings.show_exit_message,
                "show_logo": settings.show_logo,
            },
        }

        with SETTINGS_PATH.open("w") as f:
            json.dump(settings_json, f, indent=4)


    def load_language(self, language: str) -> List[str]:
        """
        Load a language word list.
        Priority:
            1. User config override (~/.config/termitype/languages/*.json)
            2. Packaged default language (termitype/data/languages/*.json)
        """

        filename = f"{language}.json"

        user_lang_dir = CONFIG_DIR / "languages"
        user_lang_path = user_lang_dir / filename

        if user_lang_path.exists():
            try:
                with user_lang_path.open("r") as f:
                    data = json.load(f)
                    return data.get("words", [])
            except Exception:
                pass

        if res.is_resource(PKG_LANGUAGES, filename):
            with res.open_text(PKG_LANGUAGES, filename) as f:
                data = json.load(f)
                return data.get("words", [])

        return []

    def load_runs(self) -> List[RunReport]:
        """
        Run history is user-modifiable, so keep it in ~/.config.
        """
        if not RUNS_PATH.exists():
            return []

        with RUNS_PATH.open("r") as f:
            data = json.load(f)
            return [RunReport.from_dict(d) for d in data.get("runs", [])]

    def save_runs(self, runs: List[RunReport]) -> None:
        data = {
            "runs": [run.as_dict for run in runs]
        }
        with RUNS_PATH.open("w") as f:
            json.dump(data, f, indent=4)

