import requests
from typing import Dict
from src.config import CONFIG

class thermometer:
    def __init__(self, verbose: bool = True):
        self.api_key = CONFIG.OPEN_WEATHER_MAP_KEY
        if not self.api_key:
            raise ValueError("API Key not found. Please set it using os.environ['OPENWEATHERMAP_API_SHARED'] = 'YOUR_API_KEY")
        self.temperature_api_url = "https://api.openweathermap.org/data/3.0/onecall"
        self.geocode_api_url = "https://api.openweathermap.org/geo/1.0/direct"
        self.verbose = verbose

    def __get_location_coordinates(self, city: str, state_abbr: str) -> Dict[str, float]:
        """
        Fetch the latitude and longitude of a given city using OpenWeatherMap API.
        Returns a dict with 'lat' and 'lon'.
        """
        params = {
            "q": f"{city},{state_abbr},USA",
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
                print(f"Found coordinates for {city}, {state_abbr}: ({lat}, {lon})")
            return {"lat": lat, "lon": lon}
        raise ValueError("Location Not Found")

    def __get_temperature_api(self, coordinates) -> float:
        """
        Fetch the 'feels like' temperature for a given city using OpenWeatherMap API.
        Returns the temperature in Fahrenheit.
        """
        # coordinates = self.__get_location_coordinates(city, state_abbr)
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
        current = data.get("current")
        if current:
            if self.verbose:
                print(f"Current Weather: {current.get('feels_like')}°F")
            return current.get("feels_like")
        
        raise ValueError("Current weather not found.")

    def find_temperature(self, city: str, state_abbr: str) -> float:
        """
        Get the 'feels like' temperature for a given city.
        Uses the specified method: 'api' or 'manual'.
        If 'api' fails, falls back to manual input.
        """

        coordinates = self.__get_location_coordinates(city, state_abbr)
        temperature = self.__get_temperature_api(coordinates)

        return temperature
