"""
Business Search                     URL === 'https://api.yelp.com/v3/businesses/search'
Business Search by Phone number     URL === 'https://api.yelp.com/v3/businesses/search/phone'
Business Match                      URL === 'https://api.yelp.com/v3/businesses/matches'
Get Business by ID                  URL === 'https://api.yelp.com/v3/businesses/{business_id}'
Search Business Transaction         URL === 'https://api.yelp.com/v3/transactions/{transaction_type}/search'
Get Business engagement metrics     URL === 'https://api.yelp.com/v3/businesses/engagement'
Get Service offerings for business  URL === 'https://api.yelp.com/v3/businesses/{business_id}/service_offerings'
"""
import requests
import json
import pandas as pd
import numpy as np
from constants import Api

YELP_API = Api.YELP_API

class Requests:

    def search_business(latitude, longitude, radius):
        offset = 0
        ENDPOINT = "https://api.yelp.com/v3/businesses/search"

        HEADERS = {
            "accept": "application/json",
            "Authorization": 'bearer %s' % YELP_API
        }

        array = []

        for x in range(0, 50, 50):
        # TODO: Change range to 200
            PARAMETERS = {
                'latitude': latitude,
                'longitude': longitude,
                'radius': radius,
                'limit': 50,
                'offset': offset
            }

            response = requests.get(url=ENDPOINT,
                                    params=PARAMETERS,
                                    headers=HEADERS)
            businesses = json.loads(response.text)
            business = businesses['businesses']
            for data in business:
                array.append(data)

            offset += 50

        return array
