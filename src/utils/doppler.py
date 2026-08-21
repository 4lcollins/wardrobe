import os

import requests

DOPPLER_SECRETS_URL = "https://api.doppler.com/v3/configs/config/secrets/download"


def import_doppler_secrets() -> None:
    token = os.getenv("DOPPLER_TOKEN", "")
    if not token:
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
