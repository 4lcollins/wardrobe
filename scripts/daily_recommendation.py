from src.core.thermometer import Thermometer
from src.core.stylist import Stylist
from src.utils.email import send_email

thermometer = Thermometer(verbose=True, city="Provo", state_abbr="UT")
stylist = Stylist(thermometer = thermometer)

city = "Provo"
state = "UT"

low_temp, high_temp = thermometer.get_low_high()
recommendation = stylist.recommend_clothing(temperature=low_temp)

message = (
    "Good Morning!\n\n"
    f"Here's today's recommendation for {city}, {state}.\n"
    "\nWEATHER\n"
    f"High feels like temperature: {high_temp}°F\n"
    f"Low feels like temperature: {low_temp}°F\n"
    "\nRECOMMENDATIONS\n"
    f"We recommend at most {recommendation['num_clothing_pieces']} clothing pieces\n"
    "Here's an example outfit:\n"
    + "\n".join(f"- {item}" for item in recommendation["clothing_options"])
    + "\n\nSincerely,\nYour Wardrobe Assistant"
)

send_email(
    subject="Daily Wardrobe Recommendation",
    body=message,
    receiver_email="landoncollins@icloud.com"
)
