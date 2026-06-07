import random
import math
from dataclasses import dataclass

from src.core.apple_ai import apple_ai
from src.core.thermometer import Thermometer

@dataclass
class ClothingRecommendation:
    insight: str

class Stylist:
    """
    Wardrobe class provides clothing recommendations based on temperature.
    """    
    CLOTHING_OPTIONS: dict[int, list[str | list[str]]] = {
            1: [
                ["Shorts"]
            ],
            2: [
                ["Short Sleeve Shirt", "Shorts"]
            ],
            3: [
                ["Short Sleeve Shirt", "Shorts", "Socks"],
                ["Short Sleeve Shirt", "Pants"],
                ["Long Sleeve Shirt", "Shorts"]
            ],
            4: [
                ["Short Sleeve Shirt", "Pants", "Socks"],
                ["Long Sleeve Shirt", "Shorts", "Socks"]
            ],
            5: [
                ["Long Sleeve Shirt", "Pants", "Socks"],
                ["Short Sleeve Shirt", "Pants", "Socks", "Jacket"]
            ],
            6: [
                ["Jacket", "Short Sleeve Shirt", "Pants", "Socks"],
                ["Long Sleeve Shirt", "Jacket", "Pants", "Socks"]
            ],
            7: [
                ["Jacket", "Long Sleeve Shirt", "Pants", "Socks"],
                ["Coat", "Short Sleeve Shirt", "Pants", "Socks"]
            ],
            8: [
                ["Jacket", "Long Sleeve Shirt", "Pants", "Socks", "Gloves"],
                ["Coat", "Long Sleeve Shirt", "Pants", "Socks"]
            ],
            9: [
                ["Coat", "Long Sleeve Shirt", "Pants", "Socks", "Gloves"]
            ]
        }

    def __init__(self, thermometer: Thermometer) -> None:
        self.thermometer = thermometer

    def _get_num_clothing_pieces(self, temperatures: list[float]) -> list[int]:
        """
        Returns the recommended number of clothing pieces for a given temperature.
        """
        nums = []
        for temp in temperatures:
            num_clothing_pieces_raw = math.ceil(11 - temp / 10)

            # Keep recommendations within the configured clothing options.
            num_clothing_pieces_adjusted = min(max(num_clothing_pieces_raw, 1), max(self.CLOTHING_OPTIONS))

            nums.append(num_clothing_pieces_adjusted)

        return nums

    def _get_clothing_options(self, num_clothing_pieces: list[int]) -> list[list[str]]:
        """
        Ensures the warmer outfit is a subset of the colder outfit 
        to avoid mid-day wardrobe changes.
        """
        # Sort so we process the coldest (most pieces) first
        # We assume index 0 is low and index 1 is high, but we sort to be safe
        low_idx = 0 if num_clothing_pieces[0] >= num_clothing_pieces[1] else 1
        high_idx = 1 - low_idx
        
        num_cold = num_clothing_pieces[low_idx]
        num_warm = num_clothing_pieces[high_idx]

        # 1. Pick the "Master" (Colder) Outfit
        master_options = self.CLOTHING_OPTIONS.get(num_cold, [])
        if master_options and isinstance(master_options[0], list):
            master_outfit = random.choice(master_options)
        else:
            master_outfit = master_options

        # 2. Find a subset for the warmer temperature
        warm_possibilities = self.CLOTHING_OPTIONS.get(num_warm, [])
        
        # If the warm temperature has multiple choices, pick the one that matches the master
        if warm_possibilities and isinstance(warm_possibilities[0], list):
            # Logic: Filter possibilities to find one where all items exist in master_outfit
            valid_subsets = [
                p for p in warm_possibilities 
                if all(item in master_outfit for item in p)
            ]
            # Fallback: If no perfect subset exists, just pick the first warm possibility
            warm_outfit = random.choice(valid_subsets) if valid_subsets else warm_possibilities[0]
        else:
            warm_outfit = warm_possibilities

        # Re-assemble in original [low, high] order
        result = [None, None]
        result[low_idx] = master_outfit
        result[high_idx] = warm_outfit
        return result

    def recommend_clothing(self) -> dict:
        """
        Recommends clothing items based on the daily high temperature.

        Args:
            temperature (float): The temperature to recommend clothing for.

        Returns:
            dict: 
                "num_clothing_pieces": Calculated number of clothing pieces to wear
                "clothing_options": Stylized clothing options based on temperature
        """
        temperatures = self.thermometer.get_low_high()
        num_clothing_pieces = self._get_num_clothing_pieces(temperatures)
        clothing_options = self._get_clothing_options(num_clothing_pieces)

        user_input = (
            f"CONTEXT:\n"
            f"Low/High Temps: {temperatures}°F\n"
            f"Morning Outfit: {clothing_options[0]}\n"
            f"Afternoon Outfit: {clothing_options[1]}\n\n"
            f"TASK:\n"
            f"You are a stylist. In a few sentence or two, explain how the user can easily transition from the morning to the afternoon "
            f"just by removing layers. Focus on the convenience of the outfit choice."
        )

        clothing_recommendation = apple_ai.generate(
            user_input=user_input,
            model_class=ClothingRecommendation
        )

        return {
            "num_clothing_pieces": num_clothing_pieces,
            "clothing_options": clothing_options,
            "insight": clothing_recommendation.insight if clothing_recommendation else None
        }
