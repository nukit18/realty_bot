from datetime import date, datetime
from sqlalchemy import sql
from asyncpg import UniqueViolationError

from utils.db_api.db_gino import db
from utils.db_api.schemas.user import User


async def add_user(id: int, fullname: str, citizenship: str, country: str, building: str, room: int,
                   end_visa: str = None,
                   payment_notification: bool = True, late_payment: bool = False,
                   visa_requirement: bool = None):
    try:
        if not end_visa is None:
            end_visa = datetime.strptime(end_visa, "%Y.%m.%d").date()
        user = User(id=id, fullname=fullname, citizenship=citizenship, country=country, building=building, room=room,
                    end_visa=end_visa,
                    payment_notification=payment_notification,
                    late_payment=late_payment, visa_requirement=visa_requirement)
        await user.create()

    except UniqueViolationError:
        pass


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def get_ids():
    users_ids = await User.select("id").gino.all()
    return users_ids


async def select_user(id: int):
    user = await User.query.where(User.id == id).gino.first()
    return user


async def change_visa_date(id: int, end_visa: str):
    end_visa_dt = datetime.strptime(end_visa, "%Y.%m.%d").date()
    student = await User.get(id)
    await student.update(end_visa=end_visa_dt, visa_requirement=True).apply()


async def late_payment_true(id: int):
    student = await User.get(id)
    await student.update(late_payment=True).apply()


async def update_payment_notification(id: int):
    student = await User.get(id)
    await student.update(payment_notification=True).apply()
