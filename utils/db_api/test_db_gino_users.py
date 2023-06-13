import asyncio
import datetime

from data import config
from utils.db_api import quick_commands_users
from utils.db_api.db_gino import db


async def test():
    await db.set_bind(config.POSTGRES_URI)
    await db.gino.drop_all()
    await db.gino.create_all()

    print("Добавляем пользователей")
    await quick_commands_users.add_user(1, "Иванов Иван Иванович", "Ближнее", "Россия", "Улица 1", 326)
    await quick_commands_users.add_user(2, "Ахметов Ахмет Ахметович", "Дальнее", "США", "Улица 1", 324, "2021.12.10", visa_requirement=True)
    await quick_commands_users.add_user(3, "Новожилов Максим Сергеевич", "Ближнее", "Россия", "Улица 2", 48)
    await quick_commands_users.add_user(4, "Архипов Семён Романович", "Дальнее", "Киргизия", "Улица 2", 48,
                                        "2021.10.02", visa_requirement=True)
    await quick_commands_users.add_user(5, "Бабин Никита Анатольевич", "Дальнее", "Таджикистан", "Улица 2", 48,
                                        "2022.01.03", visa_requirement=False)
    print("Готово")

    users = await quick_commands_users.select_all_users()
    print("Получаем пользователей ")
    print(users)

    user1 = await quick_commands_users.select_user(1)
    print(f"Получаем страну пользователя 1\n{user1.country}")

    user3 = await quick_commands_users.select_user(3)
    print(f"Получаем пользователя 3\n{user3}")

    print("Просрчока у 5 пользователя")
    await quick_commands_users.late_payment_true(5, datetime.date.today())

    user5 = await quick_commands_users.select_user(5)
    date = datetime.datetime.strptime("2021.07.02", "%Y.%m.%d").date()
    late_payment_days = date - user5.late_payment_date
    print(f"Пользователь 5 просрочил платеж на {late_payment_days.days} дней")
    user5 = await quick_commands_users.select_user(5)
    print(f"Получаем пользователя 5\n{user5}")

    print("Получаем IDs")
    ids = await quick_commands_users.get_ids()
    print(ids)


loop = asyncio.get_event_loop()
loop.run_until_complete(test())
