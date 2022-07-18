import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from config import API_TOKEN
from utils import my_value, all_value, add_cryptocurrency, delete_cryptocurrency, view_cryptocurrency
from states import Form
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

# Initialize bot
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dispatcher = Dispatcher(bot, storage=storage)

# keyboard and buttons
button_myvalue = KeyboardButton('/myvalue')
button_addvalue = KeyboardButton('/addvalue')
button_deletevalue = KeyboardButton('/deletevalue')
button_viewvalue = KeyboardButton('/viewvalue')
button_allvalue = KeyboardButton('/allvalue')
button_help = KeyboardButton('/help')

keyboard = ReplyKeyboardMarkup().add(button_myvalue, button_addvalue, button_deletevalue, button_viewvalue, button_allvalue, button_help)

# Configure logging
logging.basicConfig(level=logging.INFO)

# message sendler
@dispatcher.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    response = "Привет, я Exchange_rates бот!\nСлежу за текущим курсом криптовалют.\nЕсли что не понятно набирай /help"

    await message.answer(response, reply_markup=keyboard)

@dispatcher.message_handler(commands=['help'])
async def send_help(message: types.Message):
    response = "Список доступных команд:\n"\
                "\n/myvalue показывает список валют на которые ты подписан"\
                "\n/addvalue добавляет валюту в список"\
                "\n/deletevalue удаляет валюту из списка"\
                "\n/viewvalue просмотр курса валют в данную секунду к USDT"\
                "\n/allvalue увидеть список всех возможных криптовалют для отслеживания"

    await message.answer(response, reply_markup=keyboard)

@dispatcher.message_handler(commands=['myvalue'])
async def send_my_list_cryptocurrency(message: types.Message):
    response = my_value(message)

    await message.answer(response, reply_markup=keyboard)

@dispatcher.message_handler(commands=['allvalue'])
async def send_all_cryptocurrency(message: types.Message):
    response = all_value()

    for part in response:
        await message.answer(list(part), reply_markup=keyboard)

@dispatcher.message_handler(commands=['addvalue'])
async def send_add_cryptocurrency(message: types.Message):
    response = "Введите название криптовалюты, например SafeGalaxy"

    await Form.add_cryptocurrency.set()
    await message.answer(response, reply_markup=ReplyKeyboardRemove())

@dispatcher.message_handler(state=Form.add_cryptocurrency)
async def send_process_add_cryptocurrency(message: types.Message, state: FSMContext):
    response = add_cryptocurrency(message)

    await message.answer(response, reply_markup=keyboard)
    await state.finish()

@dispatcher.message_handler(commands=['deletevalue'])
async def send_delete_cryptocurrency(message: types.Message):
    response = "Введите название криптовалюты, например Ethereum Token"

    await Form.delete_cryptocurrency.set()
    await message.answer(response, reply_markup=ReplyKeyboardRemove())

@dispatcher.message_handler(state=Form.delete_cryptocurrency)
async def send_process_delete_cryptocurrency(message: types.Message, state: FSMContext):
    response = delete_cryptocurrency(message)

    await message.answer(response, reply_markup=keyboard)
    await state.finish()

@dispatcher.message_handler(commands=['viewvalue'])
async def send_view_cryptocurrency(message: types.Message):
    response = view_cryptocurrency(message)

    await message.answer(response, reply_markup=keyboard)
