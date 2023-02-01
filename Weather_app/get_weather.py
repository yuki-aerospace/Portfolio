import json
import requests


def get_weather(city):
    try:
        # Connect to API
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": city,
                "appid": "bc2f6b8b1f1e9ad7b1fb355778ecd9f2",
                "units": "metric",
                "lang": "en",
                },
            )
        api = json.loads(response.text)

        # get weather information
        weather = api['weather'][0]['description']
        temp = api['main']['temp']
        humidity = api['main']['humidity']
        icon = api['weather'][0]['icon']      
        
    except Exception as e:
        api = "Error..."
        
    return weather, temp, humidity, icon

