from aiogram import executor
from commands import collecting_cryptocurrency, db
from bot import disp

if __name__ == "__main__":
    db.setup()
    collecting_cryptocurrency.start()

    executor.start_polling(disp, skip_updates=True)