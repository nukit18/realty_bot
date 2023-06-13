from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from loader import _


async def new_visa_func():
    input_new_visa = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Ввести новую визу."))
            ],
        ],
        resize_keyboard=True
    )
    return input_new_visa