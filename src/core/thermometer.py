import requests
from datetime import datetime, timedelta, timezone

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

        self.low_temp = None
        self.high_temp = None

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
    def _hours_remaining_in_target_day(
        timezone_offset_seconds: int,
        now_utc: datetime | None = None,
    ) -> int:
        now_utc = now_utc or datetime.now(timezone.utc)
        target_now = now_utc + timedelta(seconds=timezone_offset_seconds)
        return max(24 - target_now.hour, 1)
 
    def get_low_high(self) -> list[float]:
        if self.low_temp and self.high_temp:
            return [self.low_temp, self.high_temp]

        forecast = self._get_forecast()
        hourly_temperature = forecast.get("hourly")

        timezone_offset_seconds = forecast.get("timezone_offset", 0)
        hours_remaining = self._hours_remaining_in_target_day(timezone_offset_seconds)
        hourly_temperature_today = hourly_temperature[:hours_remaining]

        temps_list = [h.get("feels_like") for h in hourly_temperature_today]

        self.low_temp = min(temps_list)
        self.high_temp = max(temps_list)

        return [self.low_temp, self.high_temp]
