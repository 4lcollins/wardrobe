from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class TimeOfDayPeriod:
    name: str
    start_hour: int
    end_hour: int

    def contains(self, hour: int) -> bool:
        if self.start_hour <= self.end_hour:
            return self.start_hour <= hour < self.end_hour
        return hour >= self.start_hour or hour < self.end_hour

    def is_active_or_upcoming(self, current_hour: int) -> bool:
        return self.end_hour > current_hour

DEFAULT_TIME_OF_DAY_PERIODS = [
    TimeOfDayPeriod("Morning", 7, 12),
    TimeOfDayPeriod("Afternoon", 12, 17),
    TimeOfDayPeriod("Evening", 17, 24),
]

class Calendar:
    def __init__(self):
        self.time_of_day_periods = DEFAULT_TIME_OF_DAY_PERIODS

    @property
    def active_time_of_day_periods(self) -> list[TimeOfDayPeriod]:
        current_hour = datetime.now().hour
        return [
            period for period in self.time_of_day_periods
            if period.is_active_or_upcoming(current_hour)
        ]
