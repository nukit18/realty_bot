from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _


async def citizenship_keyboard_func():
    citizenship_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Безвизовая страна"), callback_data="Ближнее")
            ],
            [
                InlineKeyboardButton(text=_("Визовая страна"), callback_data="Дальнее")
            ],
        ]
    )
    return citizenship_keyboard
