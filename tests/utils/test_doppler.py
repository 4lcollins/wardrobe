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
    monkeypatch.delenv("DOPPLER_TOKEN", raising=False)

    def fail_request(*args, **kwargs):
        raise AssertionError("Doppler should not be called without a token.")

    monkeypatch.setattr(doppler.requests, "get", fail_request)

    doppler.import_doppler_secrets()


def test_load_doppler_secrets_sets_environment(monkeypatch):
    monkeypatch.setenv("DOPPLER_TOKEN", "dp.st.test")

    def fake_get(url, params, headers, timeout):
        assert url == doppler.DOPPLER_SECRETS_URL
        assert params == {"format": "json"}
        assert headers == {"Authorization": "Bearer dp.st.test"}
        assert timeout == 10
        return FakeResponse({"SUPABASE_URL": "https://example.supabase.co"})

    monkeypatch.setattr(doppler.requests, "get", fake_get)

    doppler.import_doppler_secrets()

    assert os.environ["SUPABASE_URL"] == "https://example.supabase.co"
