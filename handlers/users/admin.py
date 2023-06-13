from aiogram import types
from aiogram.dispatcher.filters import Command

from data.config import ADMINS
from loader import dp
from utils.db_api import quick_commands_buildings


@dp.message_handler(Command("update_db"))
async def bot_start(message: types.Message):
    user_id = message.from_user.id
    if not str(user_id) in ADMINS:
        return
    await quick_commands_buildings.update_db_buildings()
    await message.answer("Готово! Данные обновлены!")
