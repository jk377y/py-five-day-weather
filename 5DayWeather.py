# used to GET weather information from the OpenWeatherMap API
import requests
# used to convert the JSON response to a Python dictionary (object)
import json
# imports the datetime class from the datetime module of the Python standard library
from datetime import datetime

# converts Kelvin to Fahrenheit
def kelvin_to_fahrenheit(kelvin_temp):
    return round((kelvin_temp - 273.15) * 9/5 + 32, 2)

# converts meters per second to miles per hour
def mps_to_mph(mps_speed):
    return round(mps_speed * 2.237, 2)

# main function
def weather():
    print("=== 5-Day Weather Forecast ===")
    # get the city from the user
    city = input("Enter the name of a city: ")

    # my API key, replace with your own (they are FREE!)
    api_key = "d01afd2806e508d282da4f840dd4696a"
    # base URL for the OpenWeatherMap API (used for fetching weather data)
    base_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"

    # make a GET request to the OpenWeatherMap API
    response = requests.get(base_url)
    # convert the JSON response to a Python dictionary (object) and store it in a variable called data
    data = json.loads(response.text)

    # check if the city was found; data.cod value will be 200 if found. 404 if not found. (see image on README.md for example)
    if data["cod"] == "404":
        print(f"Weather information not found for '{city}'. Please try again.")
    
    # if the city was found, create some variables to store the weather data
    else:
        # get all the data.list items from the api response and store them in a variable called forecasts
        forecasts = data["list"]
        # create an empty list to store the forecast dates
        forecast_dates = []
        # create an empty dictionary to store the daily forecasts
        daily_forecasts = {}

        # iterate through the forecasts (the openweathermap API returns 40 forecasts for 5 days, 1 forecast every 3 hours)
        for forecast in forecasts:
            # need to convert the forecast dt value to a date
            forecast_datetime = datetime.fromtimestamp(forecast["dt"])
            # get the date from the forecast_datetime object and store it in a variable called forecast_date
            forecast_date = forecast_datetime.date()

            # Check if the forecast date already exists
            if forecast_date not in forecast_dates:
                # if the forecast date does not exist, add it to the forecast_dates list and add the forecast date to the daily_forecasts indexed by the forecast_date
                forecast_dates.append(forecast_date)
                daily_forecasts[forecast_date] = {
                    "main_weather": forecast["weather"][0]["main"],
                    "description": forecast["weather"][0]["description"],
                    "temperature": kelvin_to_fahrenheit(forecast["main"]["temp"]),
                    "humidity": forecast["main"]["humidity"],
                    "wind_speed": mps_to_mph(forecast["wind"]["speed"])
                }

        # takes the daily_forecasts dictionary and prints the weather information for each day in the forecast
        print((f"\n5-Day Weather Forecast for '{city}':").upper())
        for date, forecast in daily_forecasts.items():
            print(f"\nDate: {date}")
            print((f"Main Weather: {forecast['main_weather']}").upper())
            print((f"Description: {forecast['description']}").upper())
            print(f"Temperature: {forecast['temperature']:.2f} °F")
            print(f"Humidity: {forecast['humidity']}%")
            print((f"Wind Speed: {forecast['wind_speed']} mph").upper())

# the weather function is called when the file is run
weather()