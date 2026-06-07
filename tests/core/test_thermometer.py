from datetime import datetime, timezone

from src.core.thermometer import Thermometer


class TestHoursRemainingInTargetDay:
    def test_uses_negative_timezone_offset(self):
        now_utc = datetime(2026, 6, 7, 12, 30, tzinfo=timezone.utc)

        assert Thermometer._hours_remaining_in_target_day(-6 * 60 * 60, now_utc) == 18

    def test_uses_positive_timezone_offset(self):
        now_utc = datetime(2026, 6, 7, 12, 30, tzinfo=timezone.utc)

        assert Thermometer._hours_remaining_in_target_day(2 * 60 * 60, now_utc) == 10


class TestGetLowHigh:
    def test_uses_target_day_slice(self, monkeypatch):
        monkeypatch.setattr(Thermometer, "_hours_remaining_in_target_day", staticmethod(lambda offset: 3))
        monkeypatch.setattr("src.core.thermometer.SETTINGS.openweathermap_key", "test-key")

        thermometer = Thermometer(city="Provo", state_abbr="UT", verbose=False)
        monkeypatch.setattr(
            thermometer,
            "_get_forecast",
            lambda: {
                "timezone_offset": -6 * 60 * 60,
                "hourly": [
                    {"feels_like": 40},
                    {"feels_like": 55},
                    {"feels_like": 50},
                    {"feels_like": 20},
                ],
            },
        )

        assert thermometer.get_low_high() == [40, 55]

    def test_reuses_cached_result(self, monkeypatch):
        monkeypatch.setattr("src.core.thermometer.SETTINGS.openweathermap_key", "test-key")

        thermometer = Thermometer(city="Provo", state_abbr="UT", verbose=False)
        thermometer.low_temp = 0
        thermometer.high_temp = 10

        assert thermometer.get_low_high() == [0, 10]
