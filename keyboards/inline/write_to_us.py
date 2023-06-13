from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _


async def write_us_keyboard_func():
    write_us_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Написать нам"), url="https://t.me/student_realty")
            ],
        ]
    )
    return write_us_keyboard
