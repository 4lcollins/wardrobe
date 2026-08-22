from dataclasses import dataclass
from datetime import date, datetime, timedelta


@dataclass(frozen=True)
class TimeOfDayPeriod:
    name: str
    start_hour: int
    end_hour: int

    def contains(self, hour: int) -> bool:
        if self.start_hour <= self.end_hour:
            return self.start_hour <= hour < self.end_hour
        return hour >= self.start_hour or hour < self.end_hour

@dataclass(frozen=True)
class ForecastPeriod:
    period: TimeOfDayPeriod
    date: date
    display_date: str

    @property
    def name(self) -> str:
        return self.period.name

    def contains(self, forecast_datetime: datetime) -> bool:
        return (
            forecast_datetime.date() == self.date
            and self.period.contains(forecast_datetime.hour)
        )

DEFAULT_TIME_OF_DAY_PERIODS = [
    TimeOfDayPeriod("Morning", 7, 12),
    TimeOfDayPeriod("Afternoon", 12, 17),
    TimeOfDayPeriod("Evening", 17, 24),
]

def _format_forecast_date(forecast_date: date, forecast_start_date: date) -> str:
    if forecast_date == forecast_start_date:
        return "Today"
    if forecast_date == forecast_start_date + timedelta(days=1):
        return "Tomorrow"
    return f"{forecast_date:%b} {forecast_date.day}"


class Calendar:
    def __init__(self):
        self.time_of_day_periods = DEFAULT_TIME_OF_DAY_PERIODS

    def map_forecast_to_periods(
        self,
        forecast_start: datetime,
        forecast_datetimes: list[datetime],
    ) -> list[ForecastPeriod]:
        """
        Return configured periods that have at least one hourly forecast row.

        Periods that already ended on the forecast-local current date are skipped.
        Future dates are limited to dates present in the returned hourly forecast.
        """
        if not forecast_datetimes:
            return []

        forecast_start_date = forecast_start.date()
        periods = []

        for forecast_datetime in forecast_datetimes:
            forecast_date = forecast_datetime.date()

            for period in self.time_of_day_periods:
                is_upcoming = (
                    forecast_date != forecast_start_date
                    or period.end_hour > forecast_start.hour
                )
                has_forecast_hour = period.contains(forecast_datetime.hour)
                is_already_added = any(
                    existing.period == period
                    and existing.date == forecast_date
                    for existing in periods
                )

                if is_upcoming and has_forecast_hour and not is_already_added:
                    periods.append(
                        ForecastPeriod(
                            period=period,
                            date=forecast_date,
                            display_date=_format_forecast_date(
                                forecast_date,
                                forecast_start_date,
                            ),
                        )
                    )

        return periods
