import asyncio

from data import config
from utils.db_api import quick_commands_users, quick_commands_buildings
from utils.db_api.db_gino import db


async def test():
    await db.set_bind(config.POSTGRES_URI)
    await db.gino.drop_all()
    await db.gino.create_all()

    print("Обновляем таблицу БД зданий")
    await quick_commands_buildings.update_db_buildings()

    print("Получаем имена")
    names = await quick_commands_buildings.get_all_names()
    print(names)

    print("Получаем список комнат на Маршала Жукова")
    rooms1 = await quick_commands_buildings.get_prices("Маршала Жукова, 3")
    print(rooms1)

    print("Получаем список комнат на Переулке Автоматики")
    rooms2 = await quick_commands_buildings.get_prices("Переулок Автоматики, 3/2")
    print(rooms2)

    print("Получаем список комнат на Красноармейской")
    rooms3 = await quick_commands_buildings.get_prices("Красноармейская, 1")
    print(rooms3)


loop = asyncio.get_event_loop()
loop.run_until_complete(test())
