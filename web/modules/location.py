from shiny import module, reactive, render, ui
from shiny.module import resolve_id

from src.core.location import Location
from src.utils.template import render_template


@module.ui
def location_ui():
    coords_id = resolve_id("user_coords")

    geolocation_js = render_template(
        "web/www/geolocation.js",
        input_id=coords_id,
    )

    return ui.div(
        ui.tags.head(
            ui.tags.script(geolocation_js),
        ),

        ui.div(
            ui.output_ui("location_status"),
            ui.input_action_button(
                "edit_location_btn",
                "✏️ Edit",
                class_="btn btn-secondary btn-compact",
            ),
            class_="location-hud",
        ),

        ui.output_ui("location_editor_panel"),

        class_="location-section",
    )


@module.server
def location_server(input, output, session):
    is_editing = reactive.Value(False)
    manual_location_error = reactive.Value(None)
    confirmed_location = reactive.Value(None)

    @reactive.effect
    @reactive.event(input.confirm_location_btn)
    def _handle_confirm_location():
        city = input.city()
        state = input.state_abb()

        if not city or not state:
            manual_location_error.set(
                "Please enter both a city and state abbreviation."
            )
            return

        try:
            loc = Location(
                city=city,
                state_abbr=state,
                verbose=True,
            )
            loc.get_coordinates()

            confirmed_location.set(loc)
            manual_location_error.set(None)
            is_editing.set(False)

        except Exception:
            confirmed_location.set(None)
            manual_location_error.set(
                f"We couldn't find {city}, {state}. Check the spelling and try again."
            )

    @reactive.effect
    @reactive.event(input.edit_location_btn)
    def _toggle_edit():
        is_editing.set(not is_editing.get())
        manual_location_error.set(None)

    @reactive.calc
    def resolved_location():
        confirmed = confirmed_location.get()

        if confirmed:
            return {
                "status": "success",
                "location": confirmed,
                "display": confirmed.display_name,
            }

        coords = input.user_coords()

        if not coords:
            return {
                "status": "loading",
                "location": None,
            }

        if "error" in coords:
            return {
                "status": "pending",
                "location": None,
            }

        if "lat" in coords and "lon" in coords:
            try:
                loc = Location.from_coords(
                    coords,
                    verbose=False,
                )

                return {
                    "status": "success",
                    "location": loc,
                    "display": loc.display_name,
                }

            except Exception:
                return {
                    "status": "pending",
                    "location": None,
                }

        return {
            "status": "loading",
            "location": None,
        }

    @reactive.effect
    def _handle_geolocation_errors():
        state_info = resolved_location()

        if (
            state_info["status"] == "pending"
            and not is_editing.get()
        ):
            is_editing.set(True)

    @output
    @render.ui
    def location_status():
        state_info = resolved_location()
        status = state_info["status"]

        if status == "loading":
            return ui.div(
                ui.span("🌎", class_="status-icon"),
                ui.span("Finding your location…"),
                class_="location-status status-loading",
            )

        if status == "success":
            return ui.div(
                ui.span("🌎", class_="status-icon"),
                ui.span(state_info["display"]),
                class_="location-status status-success",
            )

        return ui.div(
            ui.span("🌎", class_="status-icon"),
            ui.span("Location needed"),
            class_="location-status status-required",
        )

    @output
    @render.ui
    def location_editor_panel():
        state_info = resolved_location()

        if not (
            is_editing.get()
            or state_info["status"] == "pending"
        ):
            return ui.div()

        error_message = manual_location_error.get()

        error_banner = (
            ui.div(
                "⚠️ ",
                error_message,
                class_="game-alert",
            )
            if error_message
            else None
        )

        return ui.div(
            ui.div(
                ui.div(
                    ui.h4(
                        "Choose Your Location",
                        class_="panel-title",
                    ),
                    ui.p(
                        "We'll use it to tune today's weather and outfit suggestions.",
                        class_="panel-copy",
                    ),
                ),
                class_="panel-heading",
            ),

            error_banner,

            ui.layout_columns(
                ui.input_text(
                    "city",
                    "City",
                    placeholder="Salt Lake City",
                ),

                ui.input_text(
                    "state_abb",
                    "State",
                    placeholder="UT",
                ),

                col_widths={"sm": (8, 4)},
            ),

            ui.input_action_button(
                "confirm_location_btn",
                "✓ Save Location",
                class_="btn btn-secondary game-button w-100",
            ),

            class_="location-editor game-panel",
        )

    return resolved_location