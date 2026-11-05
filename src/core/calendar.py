from dataclasses import dataclass
from datetime import date, datetime, timedelta


@dataclass(frozen=True)
class TimeOfDayPeriod:
    name: str
    start_hour: float
    end_hour: float

    def contains(self, hour: int) -> bool:
        if self.start_hour <= self.end_hour:
            return self.start_hour <= hour < self.end_hour
        return hour >= self.start_hour or hour < self.end_hour


@dataclass(frozen=True)
class ForecastPeriod:
    period: TimeOfDayPeriod
    date: date
    display_date: str
    position: int = 0

    @property
    def name(self) -> str:
        return self.period.name

    def contains(self, forecast_datetime: datetime) -> bool:
        hour = forecast_datetime.hour
        period_date = forecast_datetime.date()
        if self.period.start_hour > self.period.end_hour and hour < self.period.end_hour:
            period_date -= timedelta(days=1)
        return period_date == self.date and self.period.contains(hour)


DEFAULT_TIME_OF_DAY_PERIODS = [
    TimeOfDayPeriod("Work", 7, 17),
    TimeOfDayPeriod("Evening", 17, 23),
]
DEFAULT_WEEKLY_PERIODS = {
    day: (
        [TimeOfDayPeriod("Weekend", 7, 23)]
        if day >= 5
        else DEFAULT_TIME_OF_DAY_PERIODS.copy()
    )
    for day in range(7)
}


def _format_forecast_date(forecast_date: date, forecast_start_date: date) -> str:
    if forecast_date == forecast_start_date:
        return "Today"
    if forecast_date == forecast_start_date + timedelta(days=1):
        return "Tomorrow"
    return f"{forecast_date:%b} {forecast_date.day}"


class Calendar:
    def __init__(self, periods: dict[int | str, list[TimeOfDayPeriod]] | None = None):
        self.weekly_periods = {
            day: blocks.copy() for day, blocks in DEFAULT_WEEKLY_PERIODS.items()
        }
        if periods:
            self.weekly_periods.update(
                {int(day): blocks for day, blocks in periods.items()}
            )
        self.time_of_day_periods = DEFAULT_TIME_OF_DAY_PERIODS

    def periods_for_date(self, day: date) -> list[TimeOfDayPeriod]:
        return self.weekly_periods[day.weekday()]

    def map_forecast_to_periods(
        self,
        forecast_start: datetime,
        forecast_datetimes: list[datetime],
    ) -> list[ForecastPeriod]:
        """Return scheduled blocks with at least one upcoming forecast hour."""
        periods = []
        seen = set()
        current_hour = forecast_start.replace(minute=0, second=0, microsecond=0)
        for forecast_datetime in forecast_datetimes:
            if forecast_datetime < current_hour:
                continue
            forecast_date = forecast_datetime.date()
            for period_date in (forecast_date - timedelta(days=1), forecast_date):
                for position, period in enumerate(self.periods_for_date(period_date)):
                    key = (period_date, period)
                    if key in seen:
                        continue
                    forecast_period = ForecastPeriod(
                        period,
                        period_date,
                        _format_forecast_date(period_date, forecast_start.date()),
                        position,
                    )
                    if forecast_period.contains(forecast_datetime):
                        periods.append(forecast_period)
                        seen.add(key)
        return periods
