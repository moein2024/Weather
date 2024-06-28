"""
Module providing a function printing python version.
"""
import datetime
import re
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

def normalize_dms(dms_str):
    """
    Normalize DMS string to use standard single quotes.

    Args:
        dms_str (str): DMS string.

    Returns:
        str: Normalized DMS string.
    """
    return dms_str.replace('’', "'").replace('“', '"').replace('”', '"')

def dms_to_decimal(dms_str):
    """
    Convert a DMS string to decimal degrees.

    Args:
        dms_str (str): DMS string (e.g., 35°50'58.3"N).

    Returns:
        float: Decimal degrees.
    """
    dms_pattern = re.compile(
        r'(?P<degrees>\d+)°(?P<minutes>\d+)'+"'"+r'(?P<seconds>[\d.]+)"(?P<direction>[NSEW])')
    match = dms_pattern.match(dms_str.strip())
    if not match:
        raise ValueError(f"Invalid DMS format: {dms_str}")

    degrees = int(match.group('degrees'))
    minutes = int(match.group('minutes'))
    seconds = float(match.group('seconds'))
    direction = match.group('direction')

    decimal = degrees + minutes / 60 + seconds / 3600
    if direction in ['S', 'W']:
        decimal = -decimal

    return decimal

def get_weather_forecast(lat, lon):
    """
    Fetch and display the weather forecast for a specified location.

    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.

    Returns:
        None
    """
    url = f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}'
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        print(f"Location: {data['city']['name']}, {data['city']['country']}")

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
        print(f"Error: Unable to fetch weather data. Please try again later.")

# usage:
lat_str = input("Enter latitude (e.g., 35°50'58.3\"N): ")
lon_str = input("Enter longitude (e.g., 50°59'51.7\"E): ")

lat_str = normalize_dms(lat_str)
lon_str = normalize_dms(lon_str)

latitude = dms_to_decimal(lat_str)
longitude = dms_to_decimal(lon_str)

get_weather_forecast(latitude, longitude)
