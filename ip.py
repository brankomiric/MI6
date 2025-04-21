import requests

url = "https://ipaddresser-dev.mlx.yt/ip/address"

def get_caller_ip():
    try:
        print("Fetching IP address...")
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()["ip_address"]
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None
