from pathlib import Path
from typing import Any, Dict
from yaml import safe_load

root_path = Path(__file__).parent.parent.parent.absolute()

DATABASE_PATH = "app/database/database.db"
SETTINGS_PATH = "app/data/settings.yaml"

with open(root_path / SETTINGS_PATH, "r", encoding="utf-8") as file:
    settings: Dict[str, Any] = safe_load(file)

DATABASE_CONFIG = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.sqlite",
            "credentials": {"file_path": str(root_path / DATABASE_PATH)}
        }
    },
    "apps": {
        "app": {
            "models": ["database.models"],
            "default_connection": "default"
        }
    }
}
