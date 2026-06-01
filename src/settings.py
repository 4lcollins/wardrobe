import os
from pathlib import Path
from dotenv import load_dotenv

SRC_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SRC_DIR.parent

load_dotenv(PROJECT_DIR / ".env")

APP_ENV = os.getenv("APP_ENV", "dev")

def load_simple_yaml(yaml_path: Path):
    values = {}

    if not yaml_path.exists():
        return values

    for line in yaml_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue

        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip("\"'")

    return values

def load_config():
    config_dir = SRC_DIR / "config"
    base = load_simple_yaml(config_dir / "default.yaml")
    env_file = config_dir / f"{APP_ENV}.yaml"
    if env_file.exists():
        base.update(load_simple_yaml(env_file))
    return base

class Settings:
    def __init__(self, config):
        self.app_env = APP_ENV
        self.sender_email = os.getenv("SENDER_EMAIL", config.get("sender_email", ""))
        self.icloud_sender_password = os.getenv("ICLOUD_SENDER_PASSWORD", "")
        self.openweathermap_key = os.getenv("OPENWEATHERMAP_KEY", "")

SETTINGS = Settings(load_config())
