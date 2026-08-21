from datetime import datetime, timedelta, timezone

import requests

from src.core.calendar import Calendar
from src.core.location import Location
from src.settings import SETTINGS


class Thermometer:
    def __init__(self, location: Location, verbose: bool = True):
        self.api_key = SETTINGS.openweathermap_key
        if not self.api_key:
            raise ValueError("API Key not found. Please set OPENWEATHERMAP_KEY.")

        self.temperature_api_url = "https://api.openweathermap.org/data/4.0/onecall"
        self.location = location
        self.verbose = verbose

    def _get_forecast(self) -> dict:
        coords = self.location.get_coordinates()

        params = {
            "appid": self.api_key,
            "lat": coords["lat"],
            "lon": coords["lon"],
            "units": "imperial",
        }
        endpoint_url = f"{self.temperature_api_url}/timeline/1h"
        response = requests.get(endpoint_url, params=params)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _target_datetime(timestamp: int, timezone_offset_seconds: int) -> datetime:
        return datetime.fromtimestamp(
            timestamp + timezone_offset_seconds,
            timezone.utc,
        )

    @staticmethod
    def _target_timezone_hour(timezone_offset_seconds: int) -> int:
        return (
            datetime.now(timezone.utc)
            + timedelta(seconds=timezone_offset_seconds)
        ).hour

    def get_period_temperatures(self, calendar: Calendar | None = None) -> list[dict]:
        calendar = calendar or Calendar()

        forecast = self._get_forecast()
        hourly_temperature = forecast.get("data", [])
        timezone_offset_seconds = forecast.get("timezone_offset", 0)
        timezone_hour = self._target_timezone_hour(timezone_offset_seconds)

        period_temperatures = []
        for period in calendar.active_time_of_day_periods(timezone_hour):
            temps = [
                h.get("feels_like")
                for h in hourly_temperature
                if period.contains(
                    self._target_datetime(h.get("dt"), timezone_offset_seconds).hour
                )
            ]
            if temps:
                period_temperatures.append(
                    {
                        "period": period,
                        "temperature": round(sum(temps) / len(temps), 1),
                    }
                )

        return period_temperatures
