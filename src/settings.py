import os
from pathlib import Path

from dotenv import load_dotenv

from src.utils.doppler import import_doppler_secrets

# Path resolution
SRC_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SRC_DIR.parent

# Load environment variables from .env file at project root
load_dotenv(PROJECT_DIR / ".env")
import_doppler_secrets()


class Settings:
    def __init__(self):
        self.app_env: str = os.getenv("APP_ENV", "dev")
        self.sender_email: str = os.getenv("SENDER_EMAIL", "")
        self.gmail_app_password: str = os.getenv("GMAIL_APP_PASSWORD", "")
        self.openweathermap_key: str = os.getenv("OPENWEATHERMAP_KEY", "")
        self.gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
        self.supabase_url: str = os.getenv("SUPABASE_URL", "")
        self.supabase_key: str = os.getenv("SUPABASE_KEY", "")


SETTINGS = Settings()
