import requests
from typing import Dict, List
from settings import SETTINGS
from datetime import datetime

class thermometer:
    def __init__(self, city, state_abbr, verbose: bool = True):
        self.api_key = SETTINGS.openweathermap_key
        if not self.api_key:
            raise ValueError("API Key not found. Please set it using os.environ['OPENWEATHERMAP_KEY'] = 'YOUR_API_KEY'")
        self.temperature_api_url = "https://api.openweathermap.org/data/3.0/onecall"
        self.geocode_api_url = "https://api.openweathermap.org/geo/1.0/direct"
        self.city = city
        self.state_abbr = state_abbr
        self.verbose = verbose

    def __get_location_coordinates_api(self) -> Dict[str, float]:
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

    def get_temperature(self, temp_option: str) -> Dict:
        """
        Fetch the 'feels like' temperature for a given city using OpenWeatherMap API.
        Returns the temperature in Fahrenheit.
        """
        coordinates = self.__get_location_coordinates_api()

        params = {
            "appid": self.api_key,
            "lat": coordinates["lat"],
            "lon": coordinates["lon"],
            "units": "imperial"
        }
        response = requests.get(self.temperature_api_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get("cod") == 401:
            raise ValueError("Unauthorized Access: Invalid API Key")

        today = data.get(temp_option)

        return today

    def get_low_high(self) -> List[float]:
        hourly_temperature = self.get_temperature("hourly")

        # determine hours remaining in the current local day (include current partial hour)
        hours_remaining = max(24 - datetime.now().hour, 1)
        hourly_temperature_today = hourly_temperature[:hours_remaining]

        temps_list = [h.get("feels_like") for h in hourly_temperature_today]

        low_temp = min(temps_list)
        high_temp = max(temps_list)

        return [low_temp, high_temp]