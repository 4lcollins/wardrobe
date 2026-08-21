from datetime import datetime, timedelta, timezone
from typing import TypedDict

import requests

from src.core.calendar import Calendar
from src.core.location import Location
from src.settings import SETTINGS


class ForecastHour(TypedDict):
    datetime: datetime
    feels_like: float


class Thermometer:
    def __init__(self, location: Location):
        self.api_key = SETTINGS.openweathermap_key
        if not self.api_key:
            raise ValueError("API Key not found. Please set OPENWEATHERMAP_KEY.")

        self.temperature_api_url = "https://api.openweathermap.org/data/4.0/onecall"
        self.location = location

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
    def _apply_timezone_offset(
        utc_datetime: datetime,
        timezone_offset_seconds: int,
    ) -> datetime:
        return utc_datetime + timedelta(seconds=timezone_offset_seconds)

    def _parse_forecast_hours(
        self,
        hourly_temperature: list[dict],
        timezone_offset_seconds: int,
    ) -> list[ForecastHour]:
        return [
            {
                "datetime": self._apply_timezone_offset(
                    datetime.fromtimestamp(h.get("dt"), timezone.utc),
                    timezone_offset_seconds,
                ),
                "feels_like": h.get("feels_like"),
            }
            for h in hourly_temperature
        ]

    def get_period_temperatures(self, calendar: Calendar | None = None) -> list[dict]:
        calendar = calendar or Calendar()

        forecast = self._get_forecast()
        hourly_temperature = forecast.get("data", [])
        timezone_offset_seconds = forecast.get("timezone_offset", 0)
        forecast_start = self._apply_timezone_offset(
            datetime.now(timezone.utc),
            timezone_offset_seconds,
        )
        forecast_hours = self._parse_forecast_hours(
            hourly_temperature,
            timezone_offset_seconds,
        )
        forecast_datetimes = [
            forecast_hour["datetime"]
            for forecast_hour in forecast_hours
        ]

        period_temperatures = []
        for period in calendar.map_forecast_to_periods(
            forecast_start,
            forecast_datetimes,
        ):
            temps = [
                forecast_hour["feels_like"]
                for forecast_hour in forecast_hours
                if period.contains(forecast_hour["datetime"])
            ]
            if temps:
                period_temperatures.append(
                    {
                        "period": period,
                        "temperature": round(sum(temps) / len(temps), 1),
                    }
                )

        return period_temperatures
