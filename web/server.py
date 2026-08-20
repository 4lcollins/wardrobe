from shiny import reactive, render, ui

from src.core.calendar import Calendar
from src.core.stylist import Stylist
from src.core.thermometer import Thermometer


def app_server(input, output, session):

    @render.ui
    @reactive.event(input.run_btn)
    def display_output():
        if not input.city() or not input.state_abb():
            return ui.div(
                ui.p(
                    "Enter your location on the left to review today's wardrobe plan.",
                    class_="text-muted",
                ),
            )

        try:
            calendar = Calendar()
            thermometer = Thermometer(
                city=input.city(), state_abbr=input.state_abb(), verbose=True
            )
            stylist = Stylist(thermometer=thermometer)
            rec = stylist.recommend_clothing(calendar)
        except Exception as e:
            return ui.div(f"Error retrieving recommendation: {e}", class_="alert alert-danger")

        # Weather Metrics Layout
        weather_cols = []
        for period in rec["time_periods"]:
            weather_cols.append(
                ui.card(
                    ui.div(period["name"], class_="text-muted small"),
                    ui.h3(f"{period['temperature']}°F", class_="mb-0"),
                    class_="text-center p-2",
                )
            )
        weather_grid = ui.layout_columns(*weather_cols)

        # Wardrobe Outfit Cards
        outfit_cards = []
        for period in rec["time_periods"]:
            items = [ui.tags.li(item) for item in period["clothing_options"]]
            outfit_cards.append(
                ui.card(
                    ui.card_header(f"{period['name']} Outfit"),
                    ui.p(
                        f"{len(period['clothing_options'])} garment selection(s)",
                        class_="text-muted small mb-2",
                    ),
                    ui.tags.ul(*items, class_="mb-0"),
                    class_="mb-3",
                )
            )

        # Insight Box rendering logic
        insight_text = rec.get("insight")

        if insight_text and insight_text.strip():
            insight_box = ui.div(
                ui.tags.strong("💡 Stylist Insight"),
                ui.tags.br(),
                ui.tags.em(insight_text),
                class_="insight-card",
            )
        else:
            insight_box = ui.div(
                ui.tags.small(
                    "💡 Stylist insight is currently unavailable for today's forecast.",
                    class_="text-muted italic",
                ),
                class_="mt-3 p-2 rounded border border-secondary-subtle text-center",
            )

        return ui.div(
            ui.h3(
                f"Daily Brief for ",
                ui.tags.strong(f"{input.city().title()}, {input.state_abb().upper()}"),
            ),
            ui.p(
                "Forecast-adjusted layers selected for optimal comfort.",
                class_="text-muted small",
            ),
            ui.div("🌤️ Feels-Like Forecast", class_="section-title"),
            weather_grid,
            ui.tags.hr(),
            ui.div("👕 Recommended Attire", class_="section-title"),
            *outfit_cards,
            insight_box,  # Evaluates to None when missing, cleanly hiding the UI element
        )