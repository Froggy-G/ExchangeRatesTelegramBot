import requests

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