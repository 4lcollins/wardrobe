from src.core.calendar import Calendar
from src.core.thermometer import Thermometer
from src.core.stylist import Stylist
from src.settings import SETTINGS
from src.utils.email import send_email
from src.utils.template import render_template


def run():
    calendar = Calendar()
    thermometer = Thermometer(verbose=True, city="Provo", state_abbr="UT")
    stylist = Stylist(thermometer=thermometer)

    city = "Provo"
    state = "UT"

    recommendation = stylist.recommend_clothing(calendar)

    message = render_template(
        "daily_brief.html",
        city=city,
        state=state,
        time_periods=recommendation["time_periods"],
        insight=recommendation["insight"],
    )

    send_email(
        subject="Daily Wardrobe Brief",
        body=message,
        bcc_emails=SETTINGS.recipient_emails,
    )
