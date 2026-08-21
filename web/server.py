from shiny import reactive, render

from web.modules.login import login_server
from web.modules.location import location_server
from web.modules.style import style_server
from web.ui import page_content_ui


def app_server(input, output, session):
    login_state = login_server("login")

    # Initialize the location module server and grab its resolved location getter
    resolved_location_getter = location_server("location")

    # Pass the location tracker down to the recommendation module server
    style_server("style", get_resolved_location=resolved_location_getter)

    @reactive.effect
    @reactive.event(input.logout_btn)
    def _handle_logout():
        login_state.clear()

    @output
    @render.ui
    def page_content():
        user = login_state.get_user()

        return page_content_ui(
            is_authenticated=bool(user),
            user=user,
        )
