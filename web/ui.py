from pathlib import Path

from shiny import ui

from web.modules.header import header_ui
from web.modules.location import location_ui
from web.modules.style import style_ui


css_path = Path(__file__).parent / "www" / "theme.css"


app_ui = ui.page_fluid(
    ui.include_css(css_path),

    ui.div(
        ui.div(
            header_ui("header"),
            location_ui("location"),
            class_="hero-panel",
        ),

        style_ui("style"),

        class_="app-shell",
    ),
)