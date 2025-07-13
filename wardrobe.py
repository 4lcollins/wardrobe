import random
from typing import List, Union, Dict, Any

class wardrobe:
    """
    Wardrobe class provides clothing recommendations based on temperature.
    """
    CLOTHING_RANGES: List[Dict[str, Any]] = [
            {"temp_low": 90, "temp_high": float('inf'), "num_clothing_pieces": 2},
            {"temp_low": 80, "temp_high": 90, "num_clothing_pieces": 3},
            {"temp_low": 70, "temp_high": 80, "num_clothing_pieces": 4},
            {"temp_low": 60, "temp_high": 70, "num_clothing_pieces": 5},
            {"temp_low": 45, "temp_high": 60, "num_clothing_pieces": 6},
            {"temp_low": 30, "temp_high": 45, "num_clothing_pieces": 7},
            {"temp_low": 15, "temp_high": 30, "num_clothing_pieces": 8},
            {"temp_low": float('-inf'), "temp_high": 15, "num_clothing_pieces": 9}
        ]
    
    CLOTHING_OPTIONS: Dict[int, List[Union[str, List[str]]]] = {
            2: ["Short Sleeve", "Shorts"],
            3: ["Short Sleeve", "Shorts", "Socks"],
            4: [
                ["Short Sleeve", "Pants", "Socks"],
                ["Long Sleeve", "Shorts", "Socks"]
            ],
            5: [
                ["Long Sleeve", "Pants", "Socks"],
                ["Short Sleeve", "Pants", "Socks", "Jacket"]
            ],
            6: ["Jacket", "Short Sleeve", "Pants", "Socks"],
            7: ["Jacket", "Long Sleeve", "Pants", "Socks"],
            8: ["Jacket", "Long Sleeve", "Pants", "Socks", "Gloves"],
            9: ["Coat", "Long Sleeve", "Pants", "Socks", "Gloves"]
        }

    def __init__(self) -> None:
        pass

    def _get_num_clothing_pieces(self, temperature: float) -> int:
        """
        Returns the recommended number of clothing pieces for a given temperature.

        Args:
            temperature (float): The temperature to evaluate.

        Returns:
            int: Number of clothing pieces recommended.
        """
        for range in self.CLOTHING_RANGES:
            if range["temp_low"] <= temperature < range["temp_high"]:
                return range["num_clothing_pieces"]
        # Fallback in case no range matches
        raise ValueError("Temperature out of expected range.")

    def recommend_clothing(self, daily_temp_high: float) -> List[str]:
        """
        Recommends clothing items based on the daily high temperature.

        Args:
            daily_temp_high (float): The day's high temperature.

        Returns:
            List[str]: List of recommended clothing items.
        """
        num_pieces = self._get_num_clothing_pieces(daily_temp_high)
        clothing_options = self.CLOTHING_OPTIONS.get(num_pieces, [])

        # If multiple options, randomly pick one
        if isinstance(clothing_options[0], list):
            return random.choice(clothing_options)
        else:
            return clothing_options

