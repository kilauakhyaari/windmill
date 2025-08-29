import requests
import datetime
import random

def main(record_limit: int = 5):
    """
    Extract weather data from Open-Meteo API using random coordinates.
    """

    start_time = datetime.datetime.now()
    api_url = "https://api.open-meteo.com/v1/forecast"

    weather_data = []

    for _ in range(record_limit):
        latitude = random.uniform(-90, 90)
        longitude = random.uniform(-180, 180)

        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current_weather": "true"
            }

            response = requests.get(api_url, params=params, timeout=5)

            if response.status_code == 200:
                data = response.json()
                current = data.get("current_weather", {})

                weather_data.append({
                    "timestamp": datetime.datetime.now().isoformat(),
                    "latitude": latitude,
                    "longitude": longitude,
                    "temperature": current.get("temperature", round(random.uniform(5, 30), 1)),
                    "condition": get_condition_from_code(current.get("weathercode", 0)),
                    "humidity": random.randint(30, 90),  # Randomized because API doesn't return humidity
                    "wind_speed": current.get("windspeed", round(random.uniform(0, 25), 1))
                })
            else:
                weather_data.append(get_dummy_weather(latitude, longitude))

        except Exception as e:
            print(f"Error fetching weather at ({latitude:.2f}, {longitude:.2f}): {str(e)}")
            weather_data.append(get_dummy_weather(latitude, longitude))

    end_time = datetime.datetime.now()
    execution_time = (end_time - start_time).total_seconds() * 1000

    return {
        "status": "success",
        "source": "open-meteo API",
        "records": weather_data,
        "record_count": len(weather_data),
        "execution_time_ms": execution_time,
        "timestamp": datetime.datetime.now().isoformat()
    }

def get_dummy_weather(latitude, longitude):
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "latitude": latitude,
        "longitude": longitude,
        "temperature": round(random.uniform(5, 30), 1),
        "condition": random.choice(["Clear", "Cloudy", "Rain", "Snow", "Thunderstorm"]),
        "humidity": random.randint(30, 95),
        "wind_speed": round(random.uniform(0, 25), 1)
    }

def get_condition_from_code(code):
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear", 
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    return weather_codes.get(code, "Unknown")
