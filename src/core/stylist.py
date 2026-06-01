import random
import math

class Stylist:
    """
    Wardrobe class provides clothing recommendations based on temperature.
    """    
    CLOTHING_OPTIONS: dict[int, list[str | list[str]]] = {
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

    def __init__(self, thermometer) -> None:
        self.thermometer = thermometer

    def _get_num_clothing_pieces(self, temperature: float) -> int:
        """
        Returns the recommended number of clothing pieces for a given temperature.
        """
        num_clothing_pieces_raw = math.ceil(11 - temperature / 10)

        # Keep recommendations within the configured clothing options.
        num_clothing_pieces_adjusted = min(max(num_clothing_pieces_raw, 1), max(self.CLOTHING_OPTIONS))

        return num_clothing_pieces_adjusted

    def recommend_clothing(self, temperature: float) -> list[str]:
        """
        Recommends clothing items based on the daily high temperature.

        Args:
            temperature (float): The temperature to recommend clothing for.

        Returns:
            dict: 
                "num_clothing_pieces": Calculated number of clothing pieces to wear
                "clothing_options": Stylized clothing options based on temperature
        """
        num_clothing_pieces = self._get_num_clothing_pieces(temperature)

        clothing_options = self.CLOTHING_OPTIONS.get(num_clothing_pieces, [])

        # If multiple options, randomly pick one
        if isinstance(clothing_options[0], list):
            clothing_options =  random.choice(clothing_options)

        return {
            "num_clothing_pieces": num_clothing_pieces,
            "clothing_options": clothing_options
        }
