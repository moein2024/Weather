"""
Module providing a function printing python version.
"""
import datetime
import requests
import pytz


API_KEY = '3244ac81fa8769eaffb85d6cb0cf480e'  # Replace with your API key


def degrees_to_direction(degrees):
    """
    Convert wind direction in degrees to a compass direction.

    Args:
        degrees (float): Wind direction in degrees.

    Returns:
        str: Compass direction corresponding to the given degree.
    """
    directions = {
        (337.5, 360): 'North',
        (0, 22.5): 'North',
        (22.5, 67.5): 'Northeast',
        (67.5, 112.5): 'East',
        (112.5, 157.5): 'Southeast',
        (157.5, 202.5): 'South',
        (202.5, 247.5): 'Southwest',
        (247.5, 292.5): 'West',
        (292.5, 337.5): 'Northwest'
    }

    for (start, end), direction in directions.items():
        if start <= degrees < end or (start > end and (degrees >= start or degrees < end)):
            return direction
    return 'Unknown'


def get_weather_forecast(city):
    """
    Fetch and display the weather forecast for a specified city.

    Args:
        city (str): Name of the city to get the weather forecast for.

    Returns:
        None
    """
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}'
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        print(f"City: {data['city']['name']}, {data['city']['country']}")

        # Iterate through each forecast entry in the 'list'
        for forecast in data['list']:
            weather_description = forecast['weather'][0]['description']
            if 'rain' in weather_description.lower():
                forecast_time = datetime.datetime.fromtimestamp(forecast['dt']).astimezone(
                    pytz.timezone('Asia/Tehran'))  # You Can Put Your Time Zone Like Europe/London
                print(f"\nForecast with rain for {forecast_time.strftime('%Y-%m-%d %H:%M:%S')}:")
                print(f"Weather: {weather_description}")
                print(f"Temperature: {forecast['main']['temp'] - 273.15:.2f} °C")
                print(f"Humidity: {forecast['main']['humidity']} %")
                print(f"Wind Speed: {forecast['wind']['speed']} m/s")
                print(f"Wind Direction: {degrees_to_direction(forecast['wind']['deg'])}")
    else:
        print(f"Error: City '{city}' not found. Please check the city name and try again.")


# usage:
city_name = input("Enter city name: ")
get_weather_forecast(city_name)
