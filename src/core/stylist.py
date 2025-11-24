import random
import math
from typing import List, Union, Dict, Any

class stylist:
    """
    Wardrobe class provides clothing recommendations based on temperature.
    """    
    CLOTHING_OPTIONS: Dict[int, List[Union[str, List[str]]]] = {
            1: ["Shorts"],
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

    def get_num_clothing_pieces(self, temperature: float) -> int:
        """
        Returns the recommended number of clothing pieces for a given temperature.

        Args:
            temperature (float): The temperature to evaluate.

        Returns:
            int: Number of clothing pieces recommended.
        """
        num_clothing_pieces_raw = math.ceil(11 - temperature / 10)

        # Ensure at least 1 clothing item
        num_clothing_pieces_adjusted = max(num_clothing_pieces_raw, 1)

        return num_clothing_pieces_adjusted

    def recommend_clothing(self, num_clothing_pieces: int) -> List[str]:
        """
        Recommends clothing items based on the daily high temperature.

        Args:
            daily_temp_high (float): The day's high temperature.

        Returns:
            List[str]: List of recommended clothing items.
        """
        clothing_options = self.CLOTHING_OPTIONS.get(num_clothing_pieces, [])

        # If multiple options, randomly pick one
        if isinstance(clothing_options[0], list):
            return random.choice(clothing_options)
        else:
            return clothing_options
