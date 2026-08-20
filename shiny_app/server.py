from shiny import reactive, render

from src.core.calendar import Calendar
from src.core.stylist import Stylist
from src.core.thermometer import Thermometer

SPACER = "\n----------------------------------------------------\n"


def app_server(input, output, session):

    @render.text
    @reactive.event(input.run_btn)
    def output_text():
        if not input.city() or not input.state_abb():
            return "Please enter your city and state."

        try:
            calendar = Calendar()
            thermometer = Thermometer(city=input.city(), state_abbr=input.state_abb(), verbose=True)
            stylist = Stylist(thermometer=thermometer)
            rec = stylist.recommend_clothing(calendar)
        except Exception as e:
            return f"Error fetching forecast: {e}"

        return "\n".join([
            SPACER,
            "Hi! Welcome to your Wardrobe!",
            "Let's recommend some clothing based on today's forecast.",
            SPACER,
            "Today's feels-like temperatures:",
            *[f"- {p['name']}: {p['temperature']}°F" for p in rec["time_periods"]],
            SPACER,
            "Recommended outfit pieces:",
            *[f"- {p['name']} ({p['temperature']}°F): {', '.join(p['clothing_options'])}" for p in rec["time_periods"]],
            SPACER,
            f"Stylist Insight: {rec['insight']}",
        ])