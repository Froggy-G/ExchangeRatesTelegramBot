import requests
import json

def get_exchange_rates():
    try:
        base_url = 'https://api.pancakeswap.info/api/tokens'
        raw_data = requests.get(base_url).json()
        return raw_data
    except json.decoder.JSONDecodeError:
        return "JSON Parsing error"