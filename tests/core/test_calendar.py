from datetime import datetime, timezone

from src.core.calendar import Calendar, TimeOfDayPeriod


class TestTimeOfDayPeriodContains:
    def test_contains_hour_inside_period(self):
        period = TimeOfDayPeriod("Morning", 6, 12)

        assert period.contains(6)
        assert period.contains(11)

    def test_excludes_end_hour(self):
        period = TimeOfDayPeriod("Morning", 6, 12)

        assert not period.contains(12)

    def test_contains_hour_in_overnight_period(self):
        period = TimeOfDayPeriod("Night", 22, 6)

        assert period.contains(23)
        assert period.contains(2)
        assert not period.contains(12)


class TestCalendar:
    def test_uses_default_day_periods(self):
        calendar = Calendar()

        assert [period.name for period in calendar.time_of_day_periods] == [
            "Morning",
            "Afternoon",
            "Evening",
        ]

    def test_returns_remaining_periods_for_timezone_date(self):
        calendar = Calendar()

        periods = calendar.map_forecast_to_periods(
            datetime(2026, 6, 7, 14, tzinfo=timezone.utc),
            [
                datetime(2026, 6, 7, 15, tzinfo=timezone.utc),
                datetime(2026, 6, 7, 18, tzinfo=timezone.utc),
                datetime(2026, 6, 8, 8, tzinfo=timezone.utc),
            ],
        )

        assert [period.name for period in periods] == [
            "Afternoon",
            "Evening",
            "Morning",
        ]
        assert [period.date.isoformat() for period in periods] == [
            "2026-06-07",
            "2026-06-07",
            "2026-06-08",
        ]
        assert [period.display_date for period in periods] == [
            "Today",
            "Today",
            "Tomorrow",
        ]

    def test_uses_tomorrow_periods_from_returned_forecast_hours(self):
        calendar = Calendar()
        calendar.time_of_day_periods = [
            TimeOfDayPeriod("Morning", 7, 12),
            TimeOfDayPeriod("Evening", 17, 22),
        ]

        periods = calendar.map_forecast_to_periods(
            datetime(2026, 6, 7, 23, tzinfo=timezone.utc),
            [
                datetime(2026, 6, 8, 8, tzinfo=timezone.utc),
                datetime(2026, 6, 8, 18, tzinfo=timezone.utc),
            ],
        )

        assert [period.name for period in periods] == ["Morning", "Evening"]
        assert [period.date.isoformat() for period in periods] == [
            "2026-06-08",
            "2026-06-08",
        ]
        assert [period.display_date for period in periods] == [
            "Tomorrow",
            "Tomorrow",
        ]

    def test_skips_periods_without_returned_forecast_hours(self):
        calendar = Calendar()

        periods = calendar.map_forecast_to_periods(
            datetime(2026, 6, 7, 14, tzinfo=timezone.utc),
            [
                datetime(2026, 6, 8, 8, tzinfo=timezone.utc),
            ],
        )

        assert [period.name for period in periods] == ["Morning"]
        assert [period.display_date for period in periods] == ["Tomorrow"]
