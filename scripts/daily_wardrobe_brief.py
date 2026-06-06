from src.core.thermometer import Thermometer
from src.core.stylist import Stylist
from src.utils.email import send_email

thermometer = Thermometer(verbose=True, city="Provo", state_abbr="UT")
stylist = Stylist(thermometer = thermometer)

city = "Provo"
state = "UT"

low_temp, high_temp = thermometer.get_low_high()
recommendation = stylist.recommend_clothing()

# Extract outfits for clarity
low_temp_outfit = recommendation["clothing_options"][0]
high_temp_outfit = recommendation["clothing_options"][1]

message = (
    f"Good Morning!\n\n"
    f"Here's today's recommendation for {city}, {state}.\n"
    "\n**WEATHER**\n"
    f"Low (feels like): {low_temp}°F\n"
    f"High (feels like): {high_temp}°F\n"
    "\n**WARDROBE PLAN**\n"
    f"We recommend between {recommendation['num_clothing_pieces'][1]} and {recommendation['num_clothing_pieces'][0]} pieces.\n\n"
    "**Morning / Low Temp Outfit:**\n"
    + "\n".join(f"  - {item}" for item in low_temp_outfit) + "\n\n"
    "**Midday / High Temp Outfit:**\n"
    + "\n".join(f"  - {item}" for item in high_temp_outfit) + "\n\n"
    "**Stylist Insight:**\n"
    f"{recommendation['insight']}\n"
    "\nSincerely,\nYour Wardrobe Assistant"
)

send_email(
    subject="Daily Wardrobe Brief",
    body=message,
    receiver_email="landoncollins@icloud.com"
)
