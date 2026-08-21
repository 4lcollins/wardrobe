from pathlib import Path
from typing import Any

from shiny import ui

from web.modules.home import home_ui
from web.modules.login import login_ui


css_path = Path(__file__).parent / "www" / "theme.css"


def page_content_ui(
    is_authenticated: bool,
    user: dict[str, Any] | None = None,
):
    if is_authenticated:
        return home_ui(user=user)

    return login_ui("login")


app_ui = ui.page_fluid(
    ui.include_css(css_path),
    ui.output_ui("page_content"),
)
