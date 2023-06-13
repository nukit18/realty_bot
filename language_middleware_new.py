from typing import Tuple, Any

from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from data.config import I18N_DOMAIN, LOCALES_DIR
from utils.db_api import quick_commands_language


async def get_lang(user_id):
    try:
        return await quick_commands_language.get_language(user_id)
    except:
        pass


class ACLMidlleware(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]):
        user = types.User.get_current()
        return await get_lang(user.id) or user.locale


def setup_middleware(dp):
    i18n = ACLMidlleware(I18N_DOMAIN, LOCALES_DIR)
    dp.middleware.setup(i18n)
    return i18n