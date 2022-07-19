from aiogram import executor
from utils import collecting_cryptocurrency, database
from bot import dispatcher

if __name__ == "__main__":
    database.setup()
    collecting_cryptocurrency.start()
    executor.start_polling(dispatcher, skip_updates=True)
