from src.core import (
    Calendar,
    Location,
    Stylist,
    Thermometer,
    )
from src.settings import SETTINGS
from src.utils.email import send_email
from src.utils.template import render_template


def run():
    calendar = Calendar()
    location = Location(city="Provo", state_abbr="UT")
    thermometer = Thermometer(verbose=True, location=location)
    stylist = Stylist(thermometer=thermometer)

    city = "Provo"
    state = "UT"

    recommendation = stylist.recommend_clothing(calendar)

    message = render_template(
        "src/templates/daily_outfit.html",
        use_email_css=True,
        city=city,
        state=state,
        time_periods=recommendation["time_periods"],
        insight=recommendation["insight"],
    )

    send_email(
        subject="Your Daily Outfit",
        body=message,
        bcc_emails=SETTINGS.recipient_emails,
    )
