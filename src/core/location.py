import requests
from src.settings import SETTINGS


class Location:
    def __init__(
        self,
        city: str | None = None,
        state_abbr: str | None = None,
        lat: float | None = None,
        lon: float | None = None,
        verbose: bool = True,
    ):
        self.api_key = SETTINGS.openweathermap_key
        self.geocode_api_url = "https://api.openweathermap.org/geo/1.0/direct"
        self.reverse_api_url = "https://api.openweathermap.org/geo/1.0/reverse"
        
        self.city = city
        self.state_abbr = state_abbr
        self.lat = lat
        self.lon = lon
        self.verbose = verbose
        
        # Cache for reverse-geocoded display name
        self._resolved_display_name: str | None = None

        if (self.lat is None or self.lon is None) and (not self.city or not self.state_abbr):
            raise ValueError("Must provide either (lat, lon) or (city, state_abbr)")

    @classmethod
    def from_coords(cls, coords: dict, verbose: bool = True) -> "Location":
        """Factory method to build a Location directly from browser JS input."""
        if not coords or "lat" not in coords or "lon" not in coords:
            raise ValueError("Invalid coordinates dictionary provided")
        return cls(lat=coords["lat"], lon=coords["lon"], verbose=verbose)

    def get_coordinates(self) -> dict[str, float]:
        """Returns {'lat': ..., 'lon': ...}, performing API lookup if needed."""
        if self.lat is not None and self.lon is not None:
            if self.verbose:
                print(f"Using direct coordinates: ({self.lat}, {self.lon})")
            return {"lat": self.lat, "lon": self.lon}

        return self._geocode_city_state()

    def _geocode_city_state(self) -> dict[str, float]:
        if not self.api_key:
            raise ValueError("API Key not found. Please set OPENWEATHERMAP_KEY.")

        params = {
            "q": f"{self.city},{self.state_abbr},USA",
            "limit": 1,
            "appid": self.api_key,
        }
        response = requests.get(self.geocode_api_url, params=params)
        response.raise_for_status()
        data = response.json()

        if data:
            self.lat = data[0].get("lat")
            self.lon = data[0].get("lon")
            if self.verbose:
                print(f"Geocoded {self.city}, {self.state_abbr}: ({self.lat}, {self.lon})")
            return {"lat": self.lat, "lon": self.lon}

        raise ValueError(f"Location not found for: {self.city}, {self.state_abbr}")

    def _reverse_geocode(self) -> str:
        """Perform reverse geocoding to retrieve a readable city/state from coordinates."""
        if not self.api_key or self.lat is None or self.lon is None:
            return "Current Location"

        try:
            params = {
                "lat": self.lat,
                "lon": self.lon,
                "limit": 1,
                "appid": self.api_key,
            }
            response = requests.get(self.reverse_api_url, params=params)
            response.raise_for_status()
            data = response.json()

            if data:
                city = data[0].get("name", "")
                state = data[0].get("state", "")
                if city and state:
                    return f"{city}, {state}"
                elif city:
                    return city
        except Exception as e:
            if self.verbose:
                print(f"Reverse geocoding failed: {e}")

        return "Current Location"

    @property
    def display_name(self) -> str:
        """Returns a user-friendly label for header rendering, reverse-geocoding if using raw GPS."""
        if self.city and self.state_abbr:
            return f"{self.city.title()}, {self.state_abbr.upper()}"
        
        if self._resolved_display_name is None:
            self._resolved_display_name = self._reverse_geocode()
            
        return self._resolved_display_name