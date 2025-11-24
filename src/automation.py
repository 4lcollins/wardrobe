from core.thermometer import thermometer
from core.stylist import stylist
from utils.email import send_email

my_thermometer = thermometer(verbose=True, city="Provo", state_abbr="UT")
my_stylist = stylist()

my_city = "Provo"
my_state = "UT"

low_temp, high_temp = my_thermometer.get_low_high()
num_clothing_pieces = my_stylist.get_num_clothing_pieces(temperature=low_temp)
recommendation = my_stylist.recommend_clothing(num_clothing_pieces=num_clothing_pieces)

message = (
    "Good Morning!\n\n"
    f"Here's today's recommendation for {my_city}, {my_state}.\n"
    "\nWEATHER\n"
    f"High feels like temperature: {high_temp}°F\n"
    f"Low feels like temperature: {low_temp}°F\n"
    "\nRECOMMENDATIONS\n"
    f"We recommend at most {num_clothing_pieces} clothing pieces\n"
    "Here's an example outfit:\n"
    + "\n".join(f"- {item}" for item in recommendation)
    + "\n\nSincerely,\nYour Wardrobe Assistant"
)

send_email(
    subject="Daily Wardrobe Recommendation",
    body=message,
    receiver_email="landoncollins@icloud.com"
)