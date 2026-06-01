from shiny import reactive, render

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
            thermometer = Thermometer(city=input.city(), state_abbr=input.state_abb(), verbose=True)
            low_temp, high_temp = thermometer.get_low_high()
        except Exception as e:
            lines.append(f"Error fetching temperature from API: {e}")
            return "\n".join(lines)

        stylist = Stylist(thermometer = thermometer)
        lines.extend(
            [
                spacer_text,
                f"Awesome! Today's feels-like range is {low_temp}°F to {high_temp}°F.",
                "Now, let's recommend some clothing pieces for you.",
            ]
        )
        recommendation = stylist.recommend_clothing(temperature=low_temp)

        lines.append(spacer_text)
        lines.append("Here are your recommended clothing pieces for this location:")
        for item in recommendation["clothing_options"]:
            lines.append(f"- {item}")

        return "\n".join(lines)
