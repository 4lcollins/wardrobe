import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

APP_ENV = os.getenv("APP_ENV", "ci")

def load_config():
    base = yaml.safe_load(Path("src/config/default.yaml").read_text())
    env_file = Path(f"src/config/{APP_ENV}.yaml")
    if env_file.exists():
        base.update(yaml.safe_load(env_file.read_text()) or {})
    return base

class Settings(BaseSettings):
    # core
    app_env: str = APP_ENV

    # configuration loaded from YAML
    sender_email: str

    # sensitive
    icloud_sender_password: str
    openweathermap_key: str

SETTINGS = Settings(**load_config())