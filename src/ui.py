from shiny import ui

app_ui = ui.page_fluid(
    ui.input_text("city", "Enter your city:", value=""),
    ui.input_text("state_abb", "Enter your state (e.g. UT)", value=""),
    ui.input_action_button("run_btn", "Recommend Clothing"),
    ui.output_text_verbatim("output_text")
)