from aiogram.dispatcher.filters.state import State, StatesGroup

class Form(StatesGroup):
    cryptocurrency = State()  # Will be represented in storage as 'Form:cryptocurrency'