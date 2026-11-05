from datetime import datetime, timezone

import pytest

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
    def test_calendar_accepts_weekday_keys_from_json(self):
        calendar = Calendar({
            "0": [TimeOfDayPeriod("Work", 8, 17)],
            "6": [TimeOfDayPeriod("Church", 9, 11)],
        })
        assert calendar.periods_for_date(datetime(2026, 6, 8).date())[0].name == "Work"
        assert calendar.periods_for_date(datetime(2026, 6, 14).date())[0].name == "Church"

    def test_weekday_and_weekend_overrides(self):
        schedule = {
            day: [TimeOfDayPeriod("Work", 7, 17), TimeOfDayPeriod("Evening", 17, 24)]
            for day in range(7)
        }
        schedule[0] = [TimeOfDayPeriod("Commute", 7, 9), TimeOfDayPeriod("Work", 9, 17)]
        schedule[5] = [TimeOfDayPeriod("Weekend", 9, 18)]
        schedule[6] = [TimeOfDayPeriod("Leisure", 10, 20)]
        calendar = Calendar(schedule)

        assert [period.name for period in calendar.periods_for_date(datetime(2026, 6, 8).date())] == [
            "Commute", "Work"
        ]
        assert [period.name for period in calendar.periods_for_date(datetime(2026, 6, 9).date())] == [
            "Work", "Evening"
        ]
        assert [period.name for period in calendar.periods_for_date(datetime(2026, 6, 13).date())] == ["Weekend"]
        assert [period.name for period in calendar.periods_for_date(datetime(2026, 6, 14).date())] == ["Leisure"]

    def test_weekday_overnight_block_uses_start_day(self):
        schedule = {day: [] for day in range(7)}
        schedule[5] = [TimeOfDayPeriod("Night", 22, 6)]
        calendar = Calendar(schedule)
        periods = calendar.map_forecast_to_periods(
            datetime(2026, 6, 13, 23, tzinfo=timezone.utc),
            [datetime(2026, 6, 14, 2, tzinfo=timezone.utc)],
        )
        assert [(period.name, period.date.isoformat()) for period in periods] == [
            ("Night", "2026-06-13")
        ]

    def test_custom_schedule_maps_only_returned_hours_and_overnight_block(self):
        schedule = {day: [TimeOfDayPeriod("Work", 9, 17), TimeOfDayPeriod("Night", 22, 6)] for day in range(7)}
        calendar = Calendar(schedule)
        periods = calendar.map_forecast_to_periods(
            datetime(2026, 6, 7, 23, tzinfo=timezone.utc),
            [
                datetime(2026, 6, 7, 22, tzinfo=timezone.utc),
                datetime(2026, 6, 8, 2, tzinfo=timezone.utc),
                datetime(2026, 6, 8, 10, tzinfo=timezone.utc),
            ],
        )

        assert [(period.name, period.date.isoformat()) for period in periods] == [
            ("Night", "2026-06-07"),
            ("Work", "2026-06-08"),
        ]
        assert periods[0].contains(datetime(2026, 6, 8, 2, tzinfo=timezone.utc))

    def test_uses_default_day_periods(self):
        calendar = Calendar()

        assert [period.name for period in calendar.time_of_day_periods] == [
            "Work",
            "Evening",
        ]
        assert [period.name for period in calendar.periods_for_date(datetime(2026, 6, 13).date())] == [
            "Weekend"
        ]
        weekend = calendar.periods_for_date(datetime(2026, 6, 13).date())[0]
        assert weekend.start_hour == 7
        assert weekend.end_hour == 23

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
            "Weekend",
            "Work",
        ]
        assert [period.date.isoformat() for period in periods] == [
            "2026-06-07",
            "2026-06-08",
        ]
        assert [period.display_date for period in periods] == [
            "Today",
            "Tomorrow",
        ]

    def test_uses_tomorrow_periods_from_returned_forecast_hours(self):
        custom = [TimeOfDayPeriod("Morning", 7, 12), TimeOfDayPeriod("Evening", 17, 22)]
        calendar = Calendar({day: custom for day in range(7)})

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

        assert [period.name for period in periods] == ["Work"]
        assert [period.display_date for period in periods] == ["Tomorrow"]
