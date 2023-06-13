from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _


async def cancel_keyboard_func():
    cancel_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Отменить ввод"), callback_data="cancel")
            ],
        ]
    )
    return cancel_keyboard
