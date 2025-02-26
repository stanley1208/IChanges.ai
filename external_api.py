import requests

from APIKEY import WEATHER_API_KEY
from APIKEY import TRAFFIC_API_KEY




def get_weather(city):
    """Fetches current weather condition for a given city."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()

    if response.get("weather"):
        return response['weather'][0]['description']
    return "Unknown weather condition"

def get_traffic(location):
    """Fetches real-time traffic status for a location using Google Maps API."""
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={location}&destinations={location}&key={TRAFFIC_API_KEY}"
    response = requests.get(url).json()

    if response.get("rows"):
        traffic_status = response["rows"][0]["elements"][0].get("status", "UNKNOWN")
        return traffic_status
    return "Unknown traffic status"
