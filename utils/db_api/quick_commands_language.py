from datetime import date, datetime
from sqlalchemy import sql
from asyncpg import UniqueViolationError

from utils.db_api.db_gino import db
from utils.db_api.schemas.user_lang import User_lang


async def add_user(id: int, language: str = "ru"):
    try:
        user = User_lang(id=id, language=language)
        await user.create()

    except UniqueViolationError:
        pass


async def update_language(id: int, lang: str):
    student = await User_lang.get(id)
    await student.update(language=lang).apply()


async def get_language(id: int):
    user = await User_lang.query.where(User_lang.id == id).gino.first()
    return user.language