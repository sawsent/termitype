import json
from pathlib import Path
from typing import List
from termitype.models.engine.runreport import RunReport
from termitype.models.settings import Settings
from termitype.storage.paths import SETTINGS_PATH, LANGUAGES_PATH


class StorageManager:
    def load_settings(self) -> Settings:
        with open(SETTINGS_PATH, "r") as f:
            settings_dict = json.load(f)
            return Settings(
                width = settings_dict["display"]["width"],
                height = settings_dict["display"]["height"],
                display_outline=settings_dict["display"]["outline"],
                test_word_count = settings_dict["typing"]["word_count"],
                test_text_max_width = settings_dict["typing"]["line_max_width"],
                language=settings_dict["typing"]["language"],
                show_exit_message=settings_dict["general"]["show_exit_message"],
                show_logo=settings_dict["general"]["show_logo"],
            )

    def save_settings(self, settings: Settings) -> None:
        with open(SETTINGS_PATH, "w") as f:
            settings_dict = {
                "display": {
                    "width": settings.width,
                    "height": settings.height,
                    "outline": settings.display_outline
                },
                "typing": {
                    "language": settings.language,
                    "line_max_width": settings.test_text_max_width,
                    "word_count":  settings.test_word_count,
                },
                "general": {
                    "show_exit_message": settings.show_exit_message,
                    "show_logo": settings.show_logo
                }
            }
            json.dump(settings_dict, f, indent=2)



    def load_language(self, language: str) -> List[str]:
        if Path.exists(LANGUAGES_PATH / f"{language}.json"):
            with open(LANGUAGES_PATH / f"{language}.json", "r") as f:
                language_dict = json.load(f)
                return language_dict["words"]
        else:
            return []

    def load_runs(self) -> List[RunReport]:
        return []

    def save_run(self, run: RunReport) -> bool:
        return True
