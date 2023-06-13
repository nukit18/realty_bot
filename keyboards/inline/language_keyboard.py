from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


language_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="en🇬🇧", callback_data="lang_en")
        ],
        [
            InlineKeyboardButton(text="ru🇷🇺", callback_data="lang_ru")
        ],
    ]
)