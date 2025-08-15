from environs import Env
from pathlib import Path
from typing import Any, Dict
from yaml import safe_load

root_path = Path(__file__).parent.parent.parent.absolute()

env = Env()
env.read_env()

token = env.str("TOKEN")

DATABASE_PATH = "app/database/database.db"
SETTINGS_PATH = "app/data/settings.yaml"
MESSAGES_PATH = "app/data/messages/texts.yaml"
BUTTONS_PATH = "app/data/messages/buttons.yaml"
VIDEO_PATH = "app/data/start.mp4"


with open(root_path / SETTINGS_PATH, "r", encoding="utf-8") as file:
    settings: Dict[str, Any] = safe_load(file)

with open(root_path / MESSAGES_PATH, "r", encoding="utf-8") as file:
    messages: Dict[str, Any] = safe_load(file)

with open(root_path / BUTTONS_PATH, "r", encoding="utf-8") as file:
    buttons: Dict[str, Any] = safe_load(file)


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
