import os

from src.utils import doppler


class FakeResponse:
    def __init__(self, data):
        self.data = data

    def raise_for_status(self):
        return None

    def json(self):
        return self.data


def test_load_doppler_secrets_noops_without_token(monkeypatch):
    monkeypatch.setenv("APP_ENV", "dev")
    monkeypatch.delenv("DOPPLER_TOKEN", raising=False)

    def fail_request(*args, **kwargs):
        raise AssertionError("Doppler should not be called without a token.")

    monkeypatch.setattr(doppler.requests, "get", fail_request)

    doppler.import_doppler_secrets()


def test_load_doppler_secrets_sets_environment(monkeypatch):
    monkeypatch.setenv("DOPPLER_TOKEN", "dp.st.test")
    for secret_name in doppler.REQUIRED_SECRET_NAMES:
        monkeypatch.setenv(secret_name, "set")

    def fake_get(url, params, headers, timeout):
        assert url == doppler.DOPPLER_SECRETS_URL
        assert params == {"format": "json"}
        assert headers == {"Authorization": "Bearer dp.st.test"}
        assert timeout == 10
        return FakeResponse({"SUPABASE_URL": "https://example.supabase.co"})

    monkeypatch.setattr(doppler.requests, "get", fake_get)

    doppler.import_doppler_secrets()

    assert os.environ["SUPABASE_URL"] == "https://example.supabase.co"


def test_missing_required_secrets_reports_only_missing_values(monkeypatch):
    for secret_name in doppler.REQUIRED_SECRET_NAMES:
        monkeypatch.setenv(secret_name, "set")
    monkeypatch.delenv("GMAIL_APP_PASSWORD")

    assert doppler._missing_required_secrets() == ["GMAIL_APP_PASSWORD"]


def test_import_doppler_secrets_raises_for_missing_values(monkeypatch):
    monkeypatch.setenv("DOPPLER_TOKEN", "dp.st.test")
    for secret_name in doppler.REQUIRED_SECRET_NAMES:
        monkeypatch.delenv(secret_name, raising=False)

    def fake_get(url, params, headers, timeout):
        return FakeResponse({"SUPABASE_URL": "https://example.supabase.co"})

    monkeypatch.setattr(doppler.requests, "get", fake_get)

    try:
        doppler.import_doppler_secrets()
    except RuntimeError as exc:
        message = str(exc)
    else:
        raise AssertionError("Expected missing configuration to raise RuntimeError.")

    assert "GEMINI_API_KEY" in message
    assert "SUPABASE_PROJECT_REF" in message


def test_import_doppler_secrets_requires_token_outside_dev(monkeypatch):
    monkeypatch.setenv("APP_ENV", "prod")
    monkeypatch.delenv("DOPPLER_TOKEN", raising=False)

    try:
        doppler.import_doppler_secrets()
    except RuntimeError as exc:
        message = str(exc)
    else:
        raise AssertionError("Expected missing Doppler token to raise RuntimeError.")

    assert "DOPPLER_TOKEN" in message
