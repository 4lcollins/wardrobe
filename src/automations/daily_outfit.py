import base64
from pathlib import Path

from src.core import (
    Calendar,
    Location,
    Stylist,
    Thermometer,
    )
from src.db.users import list_email_enabled_users
from src.utils.email import send_email
from src.utils.template import render_template

ASSET_DIR = Path(__file__).resolve().parent.parent.parent / "web" / "www" / "assets"
EMAIL_ICON_FILE = "apparel-sweater-sage.png"


def email_icon() -> dict[str, str]:
    path = ASSET_DIR / EMAIL_ICON_FILE
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")

    return {
        "src": f"data:image/png;base64,{encoded}",
        "alt": "Sage sweater",
    }


def run():
    users = [user for user in list_email_enabled_users() if user.get("email")]
    if not users:
        return

    calendar = Calendar()
    location = Location(city="Provo", state_abbr="UT")
    thermometer = Thermometer(location=location)
    stylist = Stylist(thermometer=thermometer)

    city = "Provo"
    state = "UT"

    recommendation = stylist.recommend_clothing(calendar)

    message = render_template(
        "src/templates/daily_outfit.html",
        use_email_css=True,
        city=city,
        state=state,
        icon=email_icon(),
        time_periods=recommendation["time_periods"],
        insight=recommendation["insight"],
    )

    for user in users:
        send_email(
            subject="Your Daily Outfit",
            body=message,
            receiver_email=user["email"],
        )
