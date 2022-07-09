import requests
import json

def get_exchange_rates():
    base_url = 'https://api.pancakeswap.info/api/tokens'
    raw_data = requests.get(base_url).json()

    data = list(raw_data['data'].values())
    
    return data

def get_names_cryptocurrency():
    result = []

    for i in get_exchange_rates():
        result.append(i['name'])

    return result