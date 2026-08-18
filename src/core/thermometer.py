import requests
from datetime import datetime, timezone

from src.core.calendar import Calendar
from src.settings import SETTINGS

class Thermometer:
    def __init__(self, city, state_abbr, verbose: bool = True):
        self.api_key = SETTINGS.openweathermap_key
        if not self.api_key:
            raise ValueError("API Key not found. Please set it using os.environ['OPENWEATHERMAP_KEY'] = 'YOUR_API_KEY'")
        self.temperature_api_url = "https://api.openweathermap.org/data/3.0/onecall"
        self.geocode_api_url = "https://api.openweathermap.org/geo/1.0/direct"
        self.city = city
        self.state_abbr = state_abbr
        self.verbose = verbose

    def __get_location_coordinates_api(self) -> dict[str, float]:
        """
        Fetch the latitude and longitude of a given city using OpenWeatherMap API.
        Returns a dict with 'lat' and 'lon'.
        """
        params = {
            "q": f"{self.city},{self.state_abbr},USA",
            "limit": 1,
            "appid": self.api_key
        }
        response = requests.get(self.geocode_api_url, params=params)
        response.raise_for_status()
        data = response.json()
        if data:
            lat = data[0].get("lat")
            lon = data[0].get("lon")
            if self.verbose:
                print(f"Found coordinates for {self.city}, {self.state_abbr}: ({lat}, {lon})")
            return {"lat": lat, "lon": lon}
        raise ValueError("Location Not Found")

    def _get_forecast(self) -> dict:
        coordinates = self.__get_location_coordinates_api()

        params = {
            "appid": self.api_key,
            "lat": coordinates["lat"],
            "lon": coordinates["lon"],
            "units": "imperial"
        }
        response = requests.get(self.temperature_api_url, params=params)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _target_datetime(timestamp: int, timezone_offset_seconds: int) -> datetime:
        return datetime.fromtimestamp(
            timestamp + timezone_offset_seconds,
            timezone.utc,
        )

    def get_period_temperatures(self, calendar: Calendar | None = None) -> list[dict]:
        calendar = calendar or Calendar()

        forecast = self._get_forecast()
        hourly_temperature = forecast.get("hourly", [])
        timezone_offset_seconds = forecast.get("timezone_offset", 0)

        period_temperatures = []
        for period in calendar.active_time_of_day_periods:
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
