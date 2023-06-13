import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.db_api.db_gino import db

from data import config

from language_middleware_new import setup_middleware

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
loop = asyncio.get_event_loop()
dp = Dispatcher(bot, storage=storage, loop=loop)

# Настроим i18n middleware для работы с многоязычностью
i18n = setup_middleware(dp)
# Создадим псевдоним для метода gettext
_ = i18n.gettext

__all__ = ["bot", "storage", "dp", "db"]
