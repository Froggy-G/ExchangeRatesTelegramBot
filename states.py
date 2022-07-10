from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    add_cryptocurrency = State()
    delete_cryptocurrency = State()