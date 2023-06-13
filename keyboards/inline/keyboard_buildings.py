import asyncio

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _

from utils.db_api import quick_commands_buildings


async def buildings_keyboard_func() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    # names = await quick_commands_buildings.get_all_names()
    # for name in names:
    #     keyboard.insert(InlineKeyboardButton(text=name, callback_data=name))
    keyboard.insert(InlineKeyboardButton(text=_("Маршала Жукова, 3"), callback_data="Маршала Жукова, 3"))
    keyboard.insert(InlineKeyboardButton(text=_("Переулок Автоматики, 3/2"), callback_data="Переулок Автоматики, 3/2"))
    keyboard.insert(InlineKeyboardButton(text=_("Красноармейская, 1"), callback_data="Красноармейская, 1"))
    return keyboard
