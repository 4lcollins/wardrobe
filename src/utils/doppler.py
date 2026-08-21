import os

import requests

DOPPLER_SECRETS_URL = "https://api.doppler.com/v3/configs/config/secrets/download"

REQUIRED_SECRET_NAMES = (
    "GEMINI_API_KEY",
    "GMAIL_APP_PASSWORD",
    "OPENWEATHERMAP_KEY",
    "SENDER_EMAIL",
    "SUPABASE_KEY",
    "SUPABASE_PROJECT_REF",
    "SUPABASE_URL",
)


def import_doppler_secrets() -> None:
    token = os.getenv("DOPPLER_TOKEN", "")
    if not token:
        if os.getenv("APP_ENV", "dev") != "dev":
            raise RuntimeError("Missing required configuration: DOPPLER_TOKEN")
        return

    response = requests.get(
        DOPPLER_SECRETS_URL,
        params={"format": "json"},
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    response.raise_for_status()

    for key, value in response.json().items():
        os.environ[key] = str(value)

    _validate_required_secrets()


def _missing_required_secrets() -> list[str]:
    return [name for name in REQUIRED_SECRET_NAMES if not os.getenv(name)]


def _validate_required_secrets() -> None:
    missing = _missing_required_secrets()
    if missing:
        raise RuntimeError(
            "Missing required configuration: " + ", ".join(sorted(missing))
        )
