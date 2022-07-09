import logging

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from config import API_TOKEN
from commands import get_exchange_rates, get_names_cryptocurrency
from db import DBHelper
from states import Form

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot, dispatcher and database
db = DBHelper()

bot = Bot(token=API_TOKEN)

storage = MemoryStorage()
disp = Dispatcher(bot, storage=storage)

# message handler/sendler
@disp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет, я Exchange_rates бот!\nСлежу за текущим курсом криптовалют.")

@disp.message_handler(commands=['myvalue'])
async def send_current_exchange_rates(message: types.Message):
    if db.get_items(message.from_user.id):
        all_items = ''

        for item in db.get_items(message.from_user.id):
            all_items += item + ', '
        await message.answer(all_items)
    else:
        await message.answer("Вы не добавили валюту для отслеживания")


@disp.message_handler(commands=['addvalue'])
async def add_cryptocurrency(message: types.Message):

    await Form.cryptocurrency.set()
    await message.answer("Введите название криптовалюты, например BTC")

@disp.message_handler(state=Form.cryptocurrency)
async def process_add_cryptocurrency(message: types.Message, state: FSMContext):

    names = get_names_cryptocurrency()

    if message.text in names:
        if message.text not in db.get_items(message.from_user.id):
            
            db.add_item(message.text, message.from_user.id)
            await message.reply(f"Вы добавили {message.text} в список отслеживаемых")
        else:
            await message.reply(f"Уже есть в списке отслеживаемых")
    else:
        await message.reply(f"Нет такой криптовалюты")
    await state.finish()


if __name__ == '__main__':
    db.setup()
    executor.start_polling(disp, skip_updates=True)