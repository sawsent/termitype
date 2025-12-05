import json
from typing import List
from termitype.models.engine.runreport import RunReport
from termitype.models.settings import Settings
from termitype.storage.paths import SETTINGS_PATH, LANGUAGES_PATH


class StorageManager:
    def __init__(self) -> None:
        pass

    def load_settings(self) -> Settings:
        with open(SETTINGS_PATH, "r") as f:
            settings_dict = json.load(f)
            return Settings(
                width = settings_dict["display"]["width"],
                height = settings_dict["display"]["height"],
                test_word_count = settings_dict["typing"]["word_count"],
                test_text_max_width = settings_dict["typing"]["line_max_width"],
                test_style=settings_dict["typing"]["display_style"]["type"],
                ahead=settings_dict["typing"]["display_style"]["ahead"],
                behind=settings_dict["typing"]["display_style"]["behind"],
                language=settings_dict["typing"]["language"]
            )

    def save_settings(self, settings: Settings) -> bool:
        print("saving settings!")
        return True

    def load_language(self, language: str) -> List[str]:
        with open(LANGUAGES_PATH / f"{language}.json", "r") as f:
            language_dict = json.load(f)
            return language_dict["words"]

    def load_runs(self) -> List[RunReport]:
        return []

    def save_run(self, run: RunReport) -> bool:
        return True
