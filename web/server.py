from web.modules.location import location_server
from web.modules.style import style_server


def app_server(input, output, session):
    # Initialize the location module server and grab its resolved location getter
    resolved_location_getter = location_server("location")
    
    # Pass the location tracker down to the recommendation module server
    style_server("style", get_resolved_location=resolved_location_getter)
