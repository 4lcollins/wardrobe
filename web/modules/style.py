from shiny import module, reactive, render, ui

from src.core import Calendar, Stylist, Thermometer


@module.ui
def style_ui():
    return ui.layout_columns(
        ui.div(
            ui.card(
                ui.card_header("Style Guide"),

                ui.p(
                    "Create today's outfit recommendations using your local weather and wardrobe preferences.",
                    class_="panel-copy",
                ),

                ui.input_action_button(
                    "run_btn",
                    "Style My Outfit",
                    class_="btn btn-primary game-button w-100",
                ),
            ),
        ),

        ui.div(
            ui.card(
                ui.card_header("Stylized Outfit"),
                ui.output_ui("display_output"),
            ),
        ),

        col_widths={"sm": (4, 8)},
        class_="recommendation-layout",
    )


@module.server
def style_server(
    input,
    output,
    session,
    get_resolved_location,
):
    @reactive.calc
    @reactive.event(input.run_btn)
    def get_recommendation_data():
        state_info = get_resolved_location()
        location = state_info.get("location")

        if not location:
            raise ValueError(
                "Choose a valid location before creating today's style recommendation."
            )

        calendar = Calendar()
        thermometer = Thermometer(
            location=location,
        )
        stylist = Stylist(thermometer=thermometer)

        recommendation = stylist.recommend_clothing(calendar)

        return {
            "rec": recommendation,
            "heading": location.display_name,
        }

    @output
    @render.ui
    def display_output():
        if input.run_btn() == 0:
            return ui.div(
                ui.h4(
                    "Ready to style your day?",
                    class_="empty-state-title",
                ),
                ui.p(
                    "Generate a recommendation to see suggested outfits for today's weather.",
                    class_="empty-state-copy",
                ),
                class_="empty-state",
            )

        try:
            data = get_recommendation_data()

        except ValueError as exc:
            return ui.div(
                ui.h4(
                    "Location needed",
                    class_="empty-state-title",
                ),
                ui.p(
                    str(exc),
                    class_="empty-state-copy",
                ),
                class_="empty-state",
            )

        except Exception:
            return ui.div(
                ui.h4(
                    "Couldn't create today's style recommendation",
                    class_="empty-state-title",
                ),
                ui.p(
                    "Something went wrong while preparing your styling suggestions. Try again in a moment.",
                    class_="empty-state-copy",
                ),
                class_="empty-state",
            )

        rec = data["rec"]
        location_heading = data["heading"]
        periods = rec["time_periods"]

        outfit_cards = []

        for index, period in enumerate(periods):
            accent_class = "morning" if index == 0 else "midday"
            clothing_options = period["clothing_options"]

            item_count = period.get(
                "num_clothing_pieces",
                len(clothing_options),
            )

            outfit_cards.append(
                ui.div(
                    ui.div(
                        ui.h4(
                            f"{period['display_date']} {period['name']}",
                            class_="outfit-title",
                        ),

                        ui.div(
                            ui.div(
                                f"{period['temperature']}°",
                                class_="outfit-temperature",
                            ),
                            ui.div(
                                "Average feels like",
                                class_="weather-caption",
                            ),
                            class_="outfit-weather",
                        ),

                        class_="outfit-header",
                    ),

                    ui.div(
                        f"{item_count} pieces",
                        class_="outfit-pieces",
                    ),

                    ui.tags.ul(
                        *(
                            ui.tags.li(item)
                            for item in clothing_options
                        ),
                        class_="outfit-list",
                    ),

                    class_=f"outfit-box {accent_class}",
                )
            )

        insight_text = (
            rec.get("insight")
            if isinstance(rec, dict)
            else None
        )

        insight_box = None

        if insight_text and str(insight_text).strip():
            insight_box = ui.div(
                ui.div(
                    "Stylist Tip",
                    class_="insight-title",
                ),

                ui.p(
                    str(insight_text),
                ),

                class_="insight",
            )

        return ui.div(
            ui.h3(
                location_heading,
                class_="brief-heading",
            ),

            ui.p(
                "Your outfit recommendation, grounded in the forecast.",
                class_="brief-subheading",
            ),

            ui.div(
                "Recommended Styles",
                class_="section-title",
            ),

            *outfit_cards,

            insight_box,

            class_="daily-brief",
        )
