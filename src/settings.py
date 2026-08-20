import os
from pathlib import Path
from dotenv import load_dotenv

# Path resolution
SRC_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SRC_DIR.parent

# Load environment variables from .env file at project root
load_dotenv(PROJECT_DIR / ".env")


def parse_email_list(value: str) -> list[str]:
    """Parses a comma- or newline-delimited string into a clean list of emails."""
    if not value:
        return []
    return [email.strip() for email in value.replace("\n", ",").split(",") if email.strip()]


class Settings:
    def __init__(self):
        self.app_env: str = os.getenv("APP_ENV", "dev")
        self.sender_email: str = os.getenv("SENDER_EMAIL", "")
        self.gmail_app_password: str = os.getenv("GMAIL_APP_PASSWORD", "")
        self.openweathermap_key: str = os.getenv("OPENWEATHERMAP_KEY", "")
        self.gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
        self.recipient_emails: list[str] = parse_email_list(os.getenv("RECIPIENT_EMAILS", ""))


SETTINGS = Settings()