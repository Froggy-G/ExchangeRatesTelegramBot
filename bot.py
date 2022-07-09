import logging

from aiogram import Bot, Dispatcher, types, executor
from config import API_TOKEN
from commands import get_exchange_rates
from db import DBHelper

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot, dispatcher and database
db = DBHelper()
bot = Bot(token=API_TOKEN)
disp = Dispatcher(bot)

# message handler/sendler
@disp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет, я Exchange_rates бот!\nСлежу за текущим курсом криптовалют.")

@disp.message_handler(commands=['myvalue'])
async def send_current_exchange_rates(message: types.Message):
    if db.get_items(message.from_user.id):
        await message.answer(db.get_items(message.from_user.id))
    else:
        await message.answer("Вы не добавили валюту для слежки")

@disp.message_handler(commands=['addvalue'])
async def add_cryptocurrency(message: types.Message):
    await message.answer("Введите название криптовалюты, например BTC")
    


if __name__ == '__main__':
    db.setup()
    executor.start_polling(disp, skip_updates=True)