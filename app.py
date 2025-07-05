from wardrobe import wardrobe
from thermometer import thermometer

if __name__ == "__main__":
    spacer_text = "\n----------------------------------------------------\n"
    print(spacer_text)
    print("Hi! Welcome to your Wardrobe!")
    print("Let's recommend some clothing based on the current temperature.")

    print(spacer_text)
    print("First, let's get your location to find the current temperature.")
    my_thermometer = thermometer(verbose=False)
    temp = my_thermometer.find_temperature(method="api")

    print(spacer_text)
    print(f"Awesome! The current temperature is {temp}°F.")
    print("Now, let's recommend some clothing pieces for you.")
    my_wardrobe = wardrobe()
    recommendation = my_wardrobe.recommend_clothing(daily_temp_high=temp)

    print(spacer_text)
    print("Here are your recommended clothing pieces for this location:")
    for item in recommendation:
        print("-", item)