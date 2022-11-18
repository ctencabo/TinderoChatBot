import requests
import json
from constants import Api as api

TOKEN = api.ABSTRACT_LOCATION_API

def get_location():
    response = requests.get(f"https://ipgeolocation.abstractapi.com/v1/?api_key={TOKEN}&fields=country,city,longitude,latitude")
    content = json.loads(response.content.decode())
    location = f'{content["city"]} , {content["country"]}'
    return location
