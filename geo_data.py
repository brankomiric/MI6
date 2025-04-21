import os
import requests
from string import Template

url_template = Template("https://ipinfo.io/$ip?token=$token")

def get_geo_data_for_ip(ip_address):
    try:
        if os.getenv("IP_INFO_TOKEN") is None:
            raise ValueError("IP_INFO_TOKEN environment variable is not set.")
        
        print("Fetching Geo data...")
        response = requests.get(url_template.substitute(ip=ip_address, token=os.getenv("IP_INFO_TOKEN")), timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    