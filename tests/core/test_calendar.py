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

    def test_filters_periods_from_timezone_hour(self):
        calendar = Calendar()

        assert [period.name for period in calendar.active_time_of_day_periods(14)] == [
            "Afternoon",
            "Evening",
        ]
