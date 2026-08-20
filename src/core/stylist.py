import random
import math
from pydantic import BaseModel
from dataclasses import dataclass

from src.core.calendar import Calendar
from src.core.thermometer import Thermometer
from src.core.llm import Prompt

class ClothingRecommendation(BaseModel):
    insight: str

class Stylist:
    """
    Stylist provides clothing recommendations based on temperature.
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
            num_clothing_pieces_adjusted = min(max(num_clothing_pieces_raw, 1), max(self.CLOTHING_OPTIONS))
            nums.append(num_clothing_pieces_adjusted)
        return nums

    def _get_clothing_option(self, num_clothing_pieces: int) -> list[str]:
        """
        Returns a random clothing option for a given number of pieces.
        """
        options = self.CLOTHING_OPTIONS.get(num_clothing_pieces, [])
        if options and isinstance(options[0], list):
            return random.choice(options)
        return options

    def _get_clothing_options(self, num_clothing_pieces: list[int]) -> list[list[str]]:
        """
        Returns clothing options for each period, ensuring warmer periods
        are subsets of the coldest period's outfit to avoid mid-day wardrobe changes.
        """
        max_pieces = max(num_clothing_pieces)
        master_outfit = self._get_clothing_option(max_pieces)

        result = []
        for num_pieces in num_clothing_pieces:
            if num_pieces == max_pieces:
                result.append(master_outfit)
                continue

            possibilities = self.CLOTHING_OPTIONS.get(num_pieces, [])
            if possibilities and isinstance(possibilities[0], list):
                valid_subsets = [
                    p for p in possibilities
                    if all(item in master_outfit for item in p)
                ]
                outfit = random.choice(valid_subsets) if valid_subsets else possibilities[0]
            else:
                outfit = possibilities

            result.append(outfit)

        return result

    def recommend_clothing(self, calendar: Calendar | None = None) -> dict:
        """
        Recommends clothing items for each configured time-of-day period.
        """
        period_temperatures = self.thermometer.get_period_temperatures(calendar)
        temperatures = [
            period_temperature["temperature"]
            for period_temperature in period_temperatures
        ]
        num_clothing_pieces = self._get_num_clothing_pieces(temperatures)
        clothing_options = self._get_clothing_options(num_clothing_pieces)

        time_periods = [
            {
                "name": period_temperature["period"].name,
                "temperature": period_temperature["temperature"],
                "num_clothing_pieces": num_pieces,
                "clothing_options": clothing_option,
            }
            for period_temperature, num_pieces, clothing_option
            in zip(period_temperatures, num_clothing_pieces, clothing_options)
        ]

        prompt_content = (
            f"CONTEXT:\n"
            f"Time of Day Periods: {time_periods}\n\n"
            f"TASK:\n"
            f"You are a stylist. In a few sentences, explain how the user can dress for each part of the day.\n\n"
            f"All of the clothing options come from the same master outfit. So, don't suggest switching actual items for other items of different materials, for example. "
            f"Focus on simple transitions between periods. Don't build or even mention transitions for periods that do not change items. "
            f"For example, don't suggest to switch to the same outfit between periods.\n\n"
            f"Only make suggestions from the clothing options given to you. Do not fabricate additional items."
        )
        clothing_recommendation = Prompt(
            model="gemini-3.5-flash",
            content=prompt_content,
            response_schema=ClothingRecommendation
        ).generate()

        return {
            "time_periods": time_periods,
            "temperatures": temperatures,
            "num_clothing_pieces": num_clothing_pieces,
            "clothing_options": clothing_options,
            "insight": clothing_recommendation.insight
        }