from typing import Any

from shiny import ui

from web.modules.location import location_ui
from web.modules.style import style_ui


def welcome_message(user: dict[str, Any] | None) -> str:
    user = user or {}
    first_name = (user.get("first_name") or "").strip()

    if first_name:
        return f"Welcome, {first_name}!"

    return "Welcome"


def header_ui(user: dict[str, Any] | None = None, module_id: str = "header"):
    return ui.div(
        ui.div(
            ui.div(
                ui.img(
                    src="assets/apparel-sweater-sage.png",
                    alt="Wardrobe",
                    class_="brand-logo",
                ),
                ui.div(
                    ui.h1(
                        "Wardrobe",
                        class_="hero-header",
                    ),
                    ui.p(
                        "Your cozy outfit guide",
                        class_="hero-kicker",
                    ),
                    class_="brand-copy",
                ),
                class_="brand-mark",
            ),

            ui.div(
                ui.p(
                    welcome_message(user),
                    class_="sub-header",
                ),
                ui.div(
                    ui.input_dark_mode(
                        id=f"{module_id}_theme_mode",
                    ),
                    class_="theme-control",
                ),
                ui.input_action_button(
                    "logout_btn",
                    "Sign Out",
                    class_="btn btn-muted btn-compact",
                ),
                class_="header-actions",
            ),

            class_="hero-top-row",
        ),
    )


def home_ui(user: dict[str, Any] | None = None):
    return ui.div(
        ui.div(
            ui.div(
                header_ui(user=user),
                location_ui("location"),
                class_="hero-panel",
            ),
            style_ui("style"),
            class_="app-shell",
        )
    )
