import os
import requests
from string import Template

url_template = Template("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/$location?unitGroup=us&include=days&key=$api_key&contentType=json")

def weather_forecast_for_location(location):
    try:
        if os.getenv("WEATHER_API_KEY") is None:
            raise ValueError("WEATHER_API_KEY environment variable is not set.")
        
        print("Fetching Weather data...")
        response = requests.get(url_template.substitute(location=location, api_key=os.getenv("WEATHER_API_KEY")), timeout=10)
        if response.status_code == 200:
            return extract_prognosis(response.json())
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    
def extract_prognosis(weather_data):
    if weather_data is None:
        return None
    
    prognosis = []
    
    for day in weather_data.get("days", []):
        temp = day.get("temp")
        conditions = day.get("conditions")
        description = day.get("description")
        prognosis.append({
            "date": day.get("datetime"),
            "temp": temp,
            "conditions": conditions,
            "description": description
        })

    return prognosis