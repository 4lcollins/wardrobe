import logging
import math
import random
from itertools import groupby

from pydantic import BaseModel

from src.core.calendar import Calendar
from src.core.thermometer import Thermometer
from src.utils.llm import Prompt

logger = logging.getLogger(__name__)


def _format_period_time(hour: float) -> str:
    minutes = round(hour * 60)
    hour_24 = (minutes // 60) % 24
    suffix = "AM" if hour_24 < 12 else "PM"
    hour_12 = hour_24 % 12 or 12
    return f"{hour_12}:{minutes % 60:02d} {suffix}"

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
        return random.choice(self.CLOTHING_OPTIONS[num_clothing_pieces])

    def _get_clothing_options(self, num_clothing_pieces: list[int]) -> list[list[str]]:
        """
        Returns clothing options for each period, ensuring warmer periods
        are subsets of the coldest period's outfit to avoid mid-day wardrobe changes.
        """
        if not num_clothing_pieces:
            return []
        max_pieces = max(num_clothing_pieces)
        master_outfit = self._get_clothing_option(max_pieces)

        result = []
        for num_pieces in num_clothing_pieces:
            if num_pieces == max_pieces:
                result.append(master_outfit)
                continue

            possibilities = self.CLOTHING_OPTIONS[num_pieces]
            valid_subsets = [
                option for option in possibilities
                if all(item in master_outfit for item in option)
            ]
            if valid_subsets:
                outfit = random.choice(valid_subsets)
            else:
                target_size = min(len(option) for option in possibilities)
                outfit = master_outfit.copy()
                for item in ("Gloves", "Coat", "Jacket", "Socks"):
                    if len(outfit) <= target_size:
                        break
                    if item in outfit:
                        outfit.remove(item)

            result.append(outfit)

        return result

    def recommend_clothing(self, calendar: Calendar | None = None) -> dict:
        """
        Recommends clothing items for each configured time-of-day period.
        """
        period_temperatures = self.thermometer.get_period_temperatures(calendar)
        time_periods = []
        for _, grouped in groupby(period_temperatures, key=lambda item: item["period"].date):
            daily_periods = list(grouped)
            sizes = self._get_num_clothing_pieces(
                [item["temperature"] for item in daily_periods]
            )
            outfits = self._get_clothing_options(sizes)
            previous = None
            for period_temperature, num_pieces, outfit in zip(daily_periods, sizes, outfits):
                removed = [item for item in previous or [] if item not in outfit]
                added = [item for item in outfit if previous is not None and item not in previous]
                changes = []
                if removed:
                    changes.append(f"Remove {', '.join(removed)}")
                if added:
                    changes.append(f"Add {', '.join(added)}")
                time_periods.append({
                    "name": period_temperature["period"].name,
                    "color_index": getattr(period_temperature["period"], "position", 0) % 4,
                    "time": (
                        f"{_format_period_time(period_temperature['period'].period.start_hour)}–"
                        f"{_format_period_time(period_temperature['period'].period.end_hour)}"
                    ),
                    "display_date": period_temperature["period"].display_date,
                    "temperature": period_temperature["temperature"],
                    "num_clothing_pieces": num_pieces,
                    "clothing_options": outfit,
                    "adjustment": "; ".join(changes),
                })
                previous = outfit

        if not time_periods:
            return {"time_periods": [], "insight": None}

        prompt_content = (
            f"CONTEXT:\n"
            f"Time of Day Periods: {time_periods}\n\n"
            f"TASK:\n"
            f"You are a stylist. In a few sentences, explain how the user can dress for each part of the day.\n\n"
            f"The clothing options for each date come from one master outfit. So, don't suggest switching actual items for other items of different materials, for example. "
            f"Focus on simple transitions between periods. Don't build or even mention transitions for periods that do not change items. "
            f"For example, don't suggest to switch to the same outfit between periods.\n\n"
            f"Only make suggestions from the clothing options given to you. Do not fabricate additional items."
        )

        insight = None
        try:
            clothing_recommendation = Prompt(
                model="gemini-3.5-flash",
                content=prompt_content,
                response_schema=ClothingRecommendation
            ).generate()
            
            if hasattr(clothing_recommendation, "parsed"):
                insight = clothing_recommendation.parsed.insight
            else:
                insight = getattr(clothing_recommendation, "insight", None)
                
        except Exception:
            logger.exception("Failed to generate stylist insight via LLM prompt.")

        return {
            "time_periods": time_periods,
            "insight": insight
        }
