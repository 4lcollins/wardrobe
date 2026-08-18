from shiny import reactive, render

from src.core.calendar import Calendar
from src.core.stylist import Stylist
from src.core.thermometer import Thermometer

spacer_text = "\n----------------------------------------------------\n"


def app_server(input, output, session):

    @render.text
    @reactive.event(input.run_btn)
    def output_text():
        if not input.city() or not input.state_abb():
            return "Please enter your city and state."

        lines = [
            spacer_text,
            "Hi! Welcome to your Wardrobe!",
            "Let's recommend some clothing based on today's forecast.",
            spacer_text,
            "First, let's get your location to find today's feels-like temperatures.",
        ]

        try:
            calendar = Calendar()
            thermometer = Thermometer(city=input.city(), state_abbr=input.state_abb(), verbose=True)
            stylist = Stylist(thermometer = thermometer)
            recommendation = stylist.recommend_clothing(calendar)
        except Exception as e:
            lines.append(f"Error fetching temperature from API: {e}")
            return "\n".join(lines)

        lines.extend(
            [
                spacer_text,
                "Awesome! Today's feels-like temperatures by time of day are:",
                *[
                    f"- {period['name']}: {period['temperature']}°F"
                    for period in recommendation["time_periods"]
                ],
                "Now, let's recommend some clothing pieces for you.",
            ]
        )

        lines.append(spacer_text)
        lines.append("Here are your recommended clothing pieces for this location:")
        for period in recommendation["time_periods"]:
            outfit = ", ".join(period["clothing_options"])
            lines.append(f"- {period['name']} ({period['temperature']}°F): {outfit}")

        return "\n".join(lines)
