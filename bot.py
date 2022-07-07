import logging

from aiogram import Bot, Dispatcher, types
from config import API_TOKEN
from commands import get_exchange_rates

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# message handler/sendler
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет, я Exchange_rates бот!\nСлежу за текущим курсом криптовалют.")

@dp.message_handler(commands=['value'])
async def send_current_exchange_rates(message: types.Message):
    result = get_exchange_rates()
    # print(result)
    await message.reply("Готово")