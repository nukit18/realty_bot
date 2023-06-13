from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from data.config import ADMINS
from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку",
            "/update_db - обновить данные таблицы со зданиями")
    else:
        text = ("Список команд: ",
                "/start - Начать диалог",
                "/help - Получить справку")
    
    await message.answer("\n".join(text))
