from pathlib import Path

root_path = Path(__file__).parent.parent.parent.absolute()

DATABASE_PATH = "app/database/database.db"

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
