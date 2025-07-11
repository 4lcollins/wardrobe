from shiny import App, ui, render, reactive
from thermometer import thermometer
from wardrobe import wardrobe

spacer_text = "\n----------------------------------------------------\n"

app_ui = ui.page_fluid(
    ui.input_text("city", "Enter your city:", value=""),
    ui.input_text("state_abb", "Enter your state (e.g. UT)", value=""),
    ui.input_action_button("run_btn", "Run"),
    ui.output_text_verbatim("output_text")
)

def server(input, output, session):
    my_thermometer = reactive.value(None)
    my_wardrobe = reactive.value(None)

    @reactive.effect
    def _init_objects():
        if my_thermometer.get() is None:
            my_thermometer.set(thermometer(verbose=True))
        if my_wardrobe.get() is None:
            my_wardrobe.set(wardrobe())

    @render.text
    @reactive.event(input.run_btn)
    def output_text():
        if not input.city() or not input.state_abb():
            return "Please enter your city and state."
        
        lines = []
        lines.append(spacer_text)
        lines.append("Hi! Welcome to your Wardrobe!")
        lines.append("Let's recommend some clothing based on the current temperature.")
        lines.append(spacer_text)
        lines.append("First, let's get your location to find the current temperature.")
        
        temp = my_thermometer.get().find_temperature(method="api", city=input.city(), state_abbr=input.state_abb())

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

app = App(app_ui, server)