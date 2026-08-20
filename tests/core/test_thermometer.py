from datetime import datetime, timezone

from src.core.calendar import TimeOfDayPeriod
from src.core.thermometer import Thermometer


class TestTargetDatetime:
    def test_uses_target_timezone_offset(self):
        timestamp = int(datetime(2026, 6, 7, 12, tzinfo=timezone.utc).timestamp())

        target_datetime = Thermometer._target_datetime(timestamp, -6 * 60 * 60)

        assert target_datetime.hour == 6


class TestGetPeriodTemperatures:
    def test_groups_temperatures_by_day_period(self, monkeypatch):
        monkeypatch.setattr("src.core.thermometer.SETTINGS.openweathermap_key", "test-key")

        thermometer = Thermometer(city="Provo", state_abbr="UT", verbose=False)
        timestamps = [
            int(datetime(2026, 6, 7, hour, tzinfo=timezone.utc).timestamp())
            for hour in [12, 13, 18, 23]
        ]
        monkeypatch.setattr(
            thermometer,
            "_get_forecast",
            lambda: {
                "timezone_offset": -6 * 60 * 60,
                "data": [
                    {"dt": timestamps[0], "feels_like": 40},
                    {"dt": timestamps[1], "feels_like": 50},
                    {"dt": timestamps[2], "feels_like": 70},
                    {"dt": timestamps[3], "feels_like": 60},
                ],
            },
        )
        calendar = type(
            "Calendar",
            (),
            {
                "active_time_of_day_periods": [
                    TimeOfDayPeriod("Morning", 6, 12),
                    TimeOfDayPeriod("Afternoon", 12, 17),
                    TimeOfDayPeriod("Evening", 17, 24),
                ]
            },
        )()

        period_temperatures = thermometer.get_period_temperatures(calendar)

        assert [
            {
                "period": item["period"].name,
                "temperature": item["temperature"],
            }
            for item in period_temperatures
        ] == [
            {"period": "Morning", "temperature": 45},
            {"period": "Afternoon", "temperature": 70},
            {"period": "Evening", "temperature": 60},
        ]
