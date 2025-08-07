from shiny import render, reactive
from src.models.thermometer import thermometer
from src.models.wardrobe_recommender import wardrobe_recommender

spacer_text = "\n----------------------------------------------------\n"

def app_server(input, output, session):
    my_thermometer = reactive.value(None)
    my_wardrobe = reactive.value(None)

    @reactive.effect
    def _init_objects():
        if my_thermometer.get() is None:
            my_thermometer.set(thermometer(verbose=True))
        if my_wardrobe.get() is None:
            my_wardrobe.set(wardrobe_recommender())

    @render.text
    @reactive.event(input.run_btn)
    def output_text():
        if not input.city() or not input.state_abb():
            return "aaaPlease enter your city and state."
        
        lines = []
        lines.append(spacer_text)
        lines.append("Hi! Welcome to your Wardrobe!")
        lines.append("Let's recommend some clothing based on the current temperature.")
        lines.append(spacer_text)
        lines.append("First, let's get your location to find the current temperature.")
        
        try:
            temp = my_thermometer.get().find_temperature(city=input.city(), state_abbr=input.state_abb())
        except Exception as e:
            lines.append(f"Error fetching temperature from API: {e}")

        print(temp)
        
        lines.append(spacer_text)
        lines.append(f"Awesome! The current temperature is {temp}°F.")
        lines.append("Now, let's recommend some clothing pieces for you.")
        recommendation = my_wardrobe.get().recommend_clothing(daily_temp_high=temp)
        
        lines.append(spacer_text)
        lines.append("Here are your recommended clothing pieces for this location:")
        for item in recommendation:
            lines.append(f"- {item}")
        
        return "\n".join(lines)