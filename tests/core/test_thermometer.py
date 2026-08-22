from datetime import datetime, timezone

from src.core.location import Location
from src.core.thermometer import Thermometer


class TestApplyTimezoneOffset:
    def test_applies_timezone_offset(self):
        utc_datetime = datetime(2026, 6, 7, 12, tzinfo=timezone.utc)

        target_datetime = Thermometer._apply_timezone_offset(
            utc_datetime,
            -6 * 60 * 60,
        )

        assert target_datetime.hour == 6


class TestGetPeriodTemperatures:
    def test_groups_temperatures_by_day_period(self, monkeypatch):
        monkeypatch.setattr("src.core.thermometer.SETTINGS.openweathermap_key", "test-key")

        location = Location(city="Provo", state_abbr="UT", verbose=False)
        thermometer = Thermometer(location=location)
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
        monkeypatch.setattr(
            "src.core.thermometer.datetime",
            type(
                "FixedDatetime",
                (datetime,),
                {
                    "now": classmethod(
                        lambda cls, tz=None: cls(2026, 6, 7, 12, tzinfo=tz)
                    ),
                },
            ),
        )

        period_temperatures = thermometer.get_period_temperatures()

        assert [
            {
                "period": item["period"].name,
                "temperature": item["temperature"],
            }
            for item in period_temperatures
        ] == [
            {"period": "Morning", "temperature": 50},
            {"period": "Afternoon", "temperature": 70},
            {"period": "Evening", "temperature": 60},
        ]
