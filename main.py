import requests
import datetime
import pytz

def degrees_to_direction(degrees):
    if degrees >= 337.5 or degrees < 22.5:
        return 'North'
    elif 22.5 <= degrees < 67.5:
        return 'Northeast'
    elif 67.5 <= degrees < 112.5:
        return 'East'
    elif 112.5 <= degrees < 157.5:
        return 'Southeast'
    elif 157.5 <= degrees < 202.5:
        return 'South'
    elif 202.5 <= degrees < 247.5:
        return 'Southwest'
    elif 247.5 <= degrees < 292.5:
        return 'West'
    elif 292.5 <= degrees < 337.5:
        return 'Northwest'
    else:
        return 'Unknown'

api_key = '3244ac81fa8769eaffb85d6cb0cf480e'  # Replace with your API key

def get_weather_forecast(city):
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(f"City: {data['city']['name']}, {data['city']['country']}")
        
        # Iterate through each forecast entry in the 'list'
        for forecast in data['list']:
            forecast_time = datetime.datetime.fromtimestamp(forecast['dt']).astimezone(pytz.timezone('Asia/Tehran'))    # You Can Put Your Time Zone Like Europe/London
            print(f"\nForecast for {forecast_time.strftime('%Y-%m-%d %H:%M:%S')}:")
            print(f"Weather: {forecast['weather'][0]['description']}")
            print(f"Temperature: {forecast['main']['temp'] - 273.15:.2f} °C")
            print(f"Humidity: {forecast['main']['humidity']} %")
            print(f"Wind Speed: {forecast['wind']['speed']} m/s")
            print(f"Wind Direction: {degrees_to_direction(forecast['wind']['deg'])}")
    else:
        print(f"Error: City '{city}' not found. Please check the city name and try again.")

#usage:
city_name = input("Enter city name: ")
get_weather_forecast(city_name)
