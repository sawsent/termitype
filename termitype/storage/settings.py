import json
from pathlib import Path
from typing import overload
from termitype.models.settings import Settings

def default_settings() -> Settings:
    return Settings()
    
def load_settings(path: Path) -> Settings:
    return Settings()

def save_settings(path: Path) -> None:
    pass
        
