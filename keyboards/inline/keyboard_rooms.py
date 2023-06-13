from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.db_api import quick_commands_buildings


async def rooms_keyboard(name: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    rooms = await quick_commands_buildings.get_prices(name)
    for room in rooms:
        keyboard.insert(InlineKeyboardButton(text=room[0], callback_data=room[0]))
    return keyboard