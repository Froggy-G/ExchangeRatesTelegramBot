import logging

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from config import API_TOKEN
from commands import get_names_cryptocurrency, compare_two_values
from db import DBHelper
from states import Form
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

# keyboard and buttons
button_myvalue = KeyboardButton('/myvalue')
button_addvalue = KeyboardButton('/addvalue')
button_deletevalue = KeyboardButton('/deletevalue')
button_viewvalue = KeyboardButton('/viewvalue')
button_help = KeyboardButton('/help')

keyboard = ReplyKeyboardMarkup()
keyboard.add(button_myvalue, button_addvalue, button_deletevalue, button_viewvalue, button_help)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot, dispatcher and database
db = DBHelper()

bot = Bot(token=API_TOKEN)

storage = MemoryStorage()
disp = Dispatcher(bot, storage=storage)

# message handler/sendler
@disp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет, я Exchange_rates бот!\nСлежу за текущим курсом криптовалют.\nЕсли что не понятно выбирай /help", reply_markup=keyboard)

@disp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply("Все очень просто:\n/myvalue показывает список валют на которые ты подписан\n/addvalue добавляет валюту в список\n/deletevalue удаляет валюту из списка\n/viewvalue просмотр курса валют в данную секунду к USDT")

@disp.message_handler(commands=['myvalue'])
async def send_current_exchange_rates(message: types.Message):
    if db.get_items(message.from_user.id):
        all_items = ''

        for item in db.get_items(message.from_user.id):
            all_items += item + ', '
        await message.answer(all_items)
    else:
        await message.answer("Вы не добавили валюту для отслеживания")

# @disp.message_handler(commands=['allvalue'])
# async def all_cryptocurrency(message: types.Message):
#     names = get_names_cryptocurrency()
#     print(names)
#     await message.answer("kek")

@disp.message_handler(commands=['addvalue'])
async def add_cryptocurrency(message: types.Message):

    await Form.add_cryptocurrency.set()
    await message.answer("Введите название криптовалюты, например SafeGalaxy")

@disp.message_handler(state=Form.add_cryptocurrency)
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

@disp.message_handler(commands=['deletevalue'])
async def delete_cryptocurrency(message: types.Message):

    await Form.delete_cryptocurrency.set()
    await message.answer("Введите название криптовалюты, например Ethereum Token")

@disp.message_handler(state=Form.delete_cryptocurrency)
async def process_delete_cryptocurrency(message: types.Message, state: FSMContext):

    names = get_names_cryptocurrency()

    if message.text in names:
        if message.text in db.get_items(message.from_user.id):
            
            db.delete_item(message.text, message.from_user.id)
            await message.reply(f"Вы удалили {message.text} из списка отслеживаемых")
        else:
            await message.reply(f"Нет такой криптовалюты в списке отслеживаемых")
    else:
        await message.reply(f"Нет такой криптовалюты")
    await state.finish()

@disp.message_handler(commands=['viewvalue'])
async def view_cryptocurrency(message: types.Message):

    if db.get_items(message.from_user.id):
        all_items = ''

        for item in db.get_items(message.from_user.id):
            all_items += item + " is " + str(compare_two_values(item)) + ' USDT\n'

        await message.answer(all_items)
    else:
        await message.answer("Нечего отслеживать :(")


if __name__ == '__main__':
    db.setup()
    executor.start_polling(disp, skip_updates=True)