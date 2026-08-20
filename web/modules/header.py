from shiny import module, ui
from shiny.module import resolve_id

from src.utils.template import render_template


@module.ui
def header_ui():
    theme_toggle_id = resolve_id("theme_mode")

    system_theme_js = render_template(
        "web/www/system_theme.js",
        toggle_id=theme_toggle_id,
    )

    return ui.div(
        ui.tags.head(
            ui.tags.script(system_theme_js),
        ),

        ui.div(
            ui.h1(
                "Wardrobe",
                class_="hero-header",
            ),

            ui.div(
                ui.input_dark_mode(
                    id=theme_toggle_id,
                    mode="light",
                ),
                class_="theme-control",
            ),

            class_="hero-top-row",
        ),

        ui.p(
            "A cozy daily outfit guide",
            class_="hero-kicker",
        ),

        ui.p(
            "Weather-aware outfit recommendations built around what feels comfortable today.",
            class_="sub-header",
        ),
    )