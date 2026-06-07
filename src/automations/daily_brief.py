from src.core.thermometer import Thermometer
from src.core.stylist import Stylist
from src.utils.email import send_email
from src.utils.template import render_template


def run(email: str):
    thermometer = Thermometer(verbose=True, city="Provo", state_abbr="UT")
    stylist = Stylist(thermometer=thermometer)

    city = "Provo"
    state = "UT"

    low_temp, high_temp = thermometer.get_low_high()
    recommendation = stylist.recommend_clothing()

    # Extract outfits for clarity
    low_temp_outfit = recommendation["clothing_options"][0]
    high_temp_outfit = recommendation["clothing_options"][1]

    message = render_template(
        "daily_brief.html",
        city=city,
        state=state,
        low_temp=low_temp,
        high_temp=high_temp,
        min_pieces=recommendation["num_clothing_pieces"][1],
        max_pieces=recommendation["num_clothing_pieces"][0],
        low_temp_outfit=low_temp_outfit,
        high_temp_outfit=high_temp_outfit,
        insight=recommendation["insight"],
    )

    send_email(
        subject="Daily Wardrobe Brief",
        body=message,
        receiver_email=email
    )