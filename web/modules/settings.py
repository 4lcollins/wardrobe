from typing import Any, Callable

from shiny import module, reactive, render, ui

from src.db.users import update_user_profile


@module.ui
def settings_ui(user: dict[str, Any] | None = None):
    user = user or {}

    return ui.div(
        ui.div(
            ui.h2("Settings", class_="panel-title"),
            ui.p("Update your profile and email preferences.", class_="panel-copy"),
            ui.output_ui("settings_message"),
            ui.div(
                ui.span("Email", class_="settings-readonly-label"),
                ui.strong(user.get("email") or "", class_="settings-readonly-value"),
                class_="settings-readonly-field",
            ),
            ui.div(
                ui.input_text(
                    "first_name",
                    "First name",
                    value=user.get("first_name") or "",
                ),
                ui.input_text(
                    "last_name",
                    "Last name",
                    value=user.get("last_name") or "",
                ),
                class_="settings-name-grid",
            ),
            ui.div(
                ui.strong("Daily outfit emails"),
                ui.input_checkbox(
                    "is_email_enabled",
                    "Enabled",
                    value=bool(user.get("is_email_enabled", True)),
                ),
                class_="settings-preference-row",
            ),
            ui.input_action_button(
                "save_settings_btn",
                "Save Changes",
                class_="btn btn-primary game-button w-100",
            ),
            class_="settings-card game-panel",
        ),
        class_="settings-wrap",
    )


@module.server
def settings_server(
    input,
    output,
    session,
    get_user: Callable[[], dict[str, Any] | None],
    set_user: Callable[[dict[str, Any]], None],
):
    message = reactive.Value(None)
    message_kind = reactive.Value("success")

    def _set_message(text: str, kind: str = "success"):
        message.set(text)
        message_kind.set(kind)

    @reactive.effect
    @reactive.event(input.save_settings_btn)
    def _save_settings():
        user = get_user() or {}
        user_id = user.get("id")

        if not user_id:
            _set_message("Profile is unavailable", "error")
            return

        first_name = input.first_name()
        last_name = input.last_name()

        if not first_name.strip():
            _set_message("First name is required", "error")
            return

        if not last_name.strip():
            _set_message("Last name is required", "error")
            return

        try:
            updated_user = update_user_profile(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                is_email_enabled=input.is_email_enabled(),
            )
        except ValueError as exc:
            _set_message(str(exc).removesuffix("."), "error")
            return
        except Exception:
            _set_message("Could not save settings", "error")
            return

        set_user({**user, **updated_user})
        _set_message("Settings saved")

    @output
    @render.ui
    def settings_message():
        text = message.get()

        if not text:
            return ui.div()

        alert_class = "game-alert settings-alert"
        if message_kind.get() == "success":
            alert_class = f"{alert_class} settings-alert-success"

        return ui.div(text, class_=alert_class)
