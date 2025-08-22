import requests
import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
MOCK_OPENWEATHER = os.getenv("MOCK_OPENWEATHER", "FALSE").upper() == "TRUE"


def get_weather(city: str) -> dict:

    if MOCK_OPENWEATHER:
        print("Mocking weather data")
        return {
            "status": "success",
            "report": f"The weather in {city} is sunny with a temperature of 25°C (77°F)."
        }
    
    if not OPENWEATHER_API_KEY:
        return {"status": "error", "error_message": "Missing OpenWeather API key."}

    url = (
        f"https://api.openweathermap.org/data/2.5/weather?q={city}"
        f"&units=metric&appid={OPENWEATHER_API_KEY}"
    )

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            return {
                "status": "error",
                "error_message": data.get("message", "Failed to fetch weather data."),
            }

        # Extract weather information
        weather_desc = data["weather"][0].get("description", "").capitalize()
        temp_c = data["main"]["temp"]
        temp_f = round((temp_c * 9 / 5) + 32, 1)
        city_name = data["name"]

        return {
            "status": "success",
            "report": f"The weather in {city_name} is {weather_desc} with a temperature of {temp_c}°C ({temp_f}°F)."
        }

    except Exception as e:
        return {"status": "error", "error_message": str(e)}
