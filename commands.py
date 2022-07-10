import requests
import json

def get_exchange_rates():
    base_url = 'https://api.pancakeswap.info/api/tokens'
    raw_data = requests.get(base_url).json()

    data = list(raw_data['data'].values())
    
    return data

def get_names_cryptocurrency():
    names = []

    for i in get_exchange_rates():
        names.append(i['name'])

    return names

def get_USDT_value():

    for i in get_exchange_rates():
        if i['name'] == "Tether USD":
            price = i['price']

    return price

def compare_two_values(second_value):
    USDT_value = get_USDT_value()

    for i in get_exchange_rates():
        if i['name'] == second_value:
            compare = float(i['price']) / float(USDT_value)
    
    return compare