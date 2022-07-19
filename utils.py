import requests
import schedule
import threading
import numpy
import math

from database import DBHelper

database = DBHelper()

# collecting cryptocurrency data service
def collecting_cryptocurrency_data():
    database.delete_rates()
    cryptocurrency_values = get_exchange_rates()

    for value in cryptocurrency_values:
        if value['name'] == "Tether USD":
            price = value['price']

    for value in cryptocurrency_values:
        database.add_rates(value['name'], str(float(value['price'])/ float(price)))

def checking_time():
    while True:
        schedule.run_pending()

schedule.every().day.at("12:00").do(collecting_cryptocurrency_data)
collecting_cryptocurrency = threading.Thread(target=checking_time)

# message handler
def my_value(message):
    if database.get_items(message.from_user.id):
        all_items = ""

        for item in database.get_items(message.from_user.id):
            all_items += f"{item}, "
        return f"Вы следите за:\n{all_items}"
    else:
        return "Вы не добавили валюту для отслеживания"

def all_value():
    names = get_names_cryptocurrency()
    names.sort()

    count_characters = len(str(names))
    count_msg = math.ceil(count_characters / 4096) # 4096 telegram limit characters
    parts_of_names = numpy.array_split(names, count_msg)

    return parts_of_names

def add_cryptocurrency(message):
    names = get_names_cryptocurrency()

    if message.text in names:
        if message.text not in database.get_items(message.from_user.id):
            database.add_item(message.text, message.from_user.id)
            return f"Вы добавили {message.text} в список отслеживаемых"
        else:
            return "Уже есть в списке отслеживаемых"
    else:
        return "Нет такой криптовалюты"

def delete_cryptocurrency(message):
    names = get_names_cryptocurrency()

    if message.text in names:
        if message.text in database.get_items(message.from_user.id):
            database.delete_item(message.text, message.from_user.id)
            return f"Вы удалили {message.text} из списка отслеживаемых"
        else:
            return "Нет такой криптовалюты в списке отслеживаемых"
    else:
        return "Нет такой криптовалюты"

def view_cryptocurrency(message):
    if database.get_items(message.from_user.id):
        all_items = ""
        cryptocurrency_values = get_exchange_rates()
        data = database.get_rates()

        for value in cryptocurrency_values:
            if value['name'] == "Tether USD":
                price = value['price']
        
        for item in database.get_items(message.from_user.id):
            for value in cryptocurrency_values:
                if value['name'] == item:
                    value_in_usdt = float(value['price']) / float(price)
                    if item in data:
                        old_price = float(data[item])
                        percent = 100 * value_in_usdt / old_price
                        dynamic = round(percent - 100, 2)
                        all_items += f"{item} = {str(value_in_usdt)} USDT {str(dynamic)}%\n"
                    else:
                        all_items += f"{item} = {str(value_in_usdt)} USDT\n"
        return f"Курс и динамика за 24 часа:\n{all_items}"
    else:
        return "Нечего отслеживать :("

# supporting functions
def get_exchange_rates():
    base_url = 'https://api.pancakeswap.info/api/tokens'
    raw_data = requests.get(base_url).json()

    data = list(raw_data['data'].values())
    return data

def get_names_cryptocurrency():
    names = []

    for name in get_exchange_rates():
        names.append(name['name'])
    return names
    