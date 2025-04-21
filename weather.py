import os
import requests
from string import Template

url_template = Template("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/$location?unitGroup=us&include=days&key=$api_key&contentType=json")

def weather_forecast_for_location(location):
    try:
        if os.getenv("WEATHER_API_KEY") is None:
            raise ValueError("WEATHER_API_KEY environment variable is not set.")
        
        print("Fetching Geo data...")
        response = requests.get(url_template.substitute(location=location, api_key=os.getenv("WEATHER_API_KEY")), timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None