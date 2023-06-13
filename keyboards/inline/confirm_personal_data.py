from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _


async def confirm_personal_keyboard_func(lang):
    confirm_personal_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Да", locale=lang), callback_data="personal_yes")
            ],
            [
                InlineKeyboardButton(text=_("Нет", locale=lang), callback_data="personal_no")
            ],
        ]
    )
    return confirm_personal_keyboard
