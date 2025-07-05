import requests
import keyring
from typing import Optional, Dict

class thermometer:
    def __init__(self, verbose: bool = True):
        self.api_key = keyring.get_password("OpenWeatherMap", "api_key")
        if not self.api_key:
            raise ValueError("API Key not found. Please set it using keyring.set_password('OpenWeatherMap', 'api_key', 'YOUR_API_KEY')")
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

    def __get_temperature_api(self, city: str, state_abbr: str) -> float:
        """
        Fetch the 'feels like' temperature for a given city using OpenWeatherMap API.
        Returns the temperature in Fahrenheit.
        """
        coordinates = self.__get_location_coordinates(city, state_abbr)
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
                print(f"Current Weather: {current}")
            return current.get("feels_like")
        raise ValueError("Current weather not found.")

    def __get_temperature_manual(self, city: str) -> float:
        """
        Manually input the 'feels like' temperature for a given city.
        Returns the temperature in Fahrenheit.
        """
        while True:
            try:
                temp = float(input(f"Enter the 'feels like' temperature in {city} (°F): "))
                return temp
            except ValueError:
                print("Invalid temperature input. Please enter a valid number.")

    def find_temperature(self, method: str = "api", city: Optional[str] = None, state_abbr: Optional[str] = None) -> float:
        """
        Get the 'feels like' temperature for a given city.
        Uses the specified method: 'api' or 'manual'.
        If 'api' fails, falls back to manual input.
        """
        if not city:
            city = input("Enter your city name (e.g. \"Salt Lake City\"): ")
        if not state_abbr:
            state_abbr = input("Enter your state abbreviation (e.g. \"UT\"): ")

        if method == "api":
            try:
                temperature = self.__get_temperature_api(city, state_abbr)
                if self.verbose:
                    print(f"Fetched temperature from API: {temperature}°F")
                return temperature
            except Exception as e:
                print(f"Error fetching temperature from API: {e}")

        return self.__get_temperature_manual(city)
