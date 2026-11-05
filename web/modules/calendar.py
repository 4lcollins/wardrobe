import json
from typing import Any, Callable

from shiny import module, reactive, render, ui

from src.core.calendar import DEFAULT_WEEKLY_PERIODS
from src.db.calendar import save_week_template

DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
DEFAULTS = {
    str(day): [
        {"name": period.name, "start_hour": period.start_hour, "end_hour": period.end_hour}
        for period in periods
    ]
    for day, periods in DEFAULT_WEEKLY_PERIODS.items()
}


@module.ui
def calendar_ui(template: dict[str, Any] | None = None):
    template_json = json.dumps(template or DEFAULTS).replace("</", "<\\/")
    return ui.div(
        ui.h2("Weekly Calendar", class_="panel-title"),
        ui.p("Drag a block to move it. Drag its lower edge to change its duration."),
        ui.div(
            ui.div(id="calendar-editor", **{"data-template": template_json}),
            ui.div(ui.input_text("calendar_data", label="", value=""), style="display:none;"),
            class_="calendar-editor-wrap",
        ),
        ui.output_ui("calendar_message"),
        ui.input_action_button(
            "save_calendar", "Save Calendar", class_="btn btn-primary game-button"
        ),
    )


@module.server
def calendar_server(input, output, session, get_user: Callable[[], dict[str, Any] | None]):
    message = reactive.Value("")

    @reactive.effect
    @reactive.event(input.save_calendar)
    def save():
        user_id = (get_user() or {}).get("id")
        if not user_id:
            message.set("Profile is unavailable.")
            return
        try:
            template = json.loads(input.calendar_data())
            for day, blocks in template.items():
                if not 0 <= int(day) < 7:
                    raise ValueError("Choose a valid day.")
                occupied = set()
                for block in blocks:
                    start = float(block["start_hour"])
                    end = float(block["end_hour"])
                    if not block["name"].strip() or not 0 <= start < end <= 24:
                        raise ValueError("Each block needs a name and a valid time range.")
                    slots = {slot for slot in range(48) if start <= slot / 2 < end}
                    if occupied & slots:
                        raise ValueError("Blocks on the same day cannot overlap.")
                    occupied.update(slots)
            save_week_template(user_id, template)
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            message.set(str(exc) or "Review the calendar blocks and try again.")
            return
        except Exception:
            message.set("Could not save calendar.")
            return
        message.set("Calendar saved.")

    @output
    @render.ui
    def calendar_message():
        return ui.p(message.get(), class_="calendar-message")
