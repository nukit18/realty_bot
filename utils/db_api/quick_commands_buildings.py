from datetime import date, datetime

from asyncpg import UniqueViolationError

from utils.db_api.db_gino import db
from utils.excel_api.excel_commands import get_MJ, get_PA, get_KA
from utils.db_api.schemas.buildings import Building


async def update_db_buildings():
    try:
        building1_info = await get_MJ()
        build1 = await Building.get(1)
        await build1.update(list=building1_info[1]).apply()

        building2_info = await get_PA()
        build2 = await Building.get(2)
        await build2.update(list=building2_info[1]).apply()

        building3_info = await get_KA()
        build3 = await Building.get(3)
        await build3.update(list=building3_info[1]).apply()
    except UniqueViolationError:
        pass


async def create_db_buildings():
    try:
        building1_info = await get_MJ()
        build1 = Building(id=1, name=building1_info[0], list=building1_info[1])
        await build1.create()
        building2_info = await get_PA()
        build2 = Building(id=2, name=building2_info[0], list=building2_info[1])
        await build2.create()
        building3_info = await get_KA()
        build3 = Building(id=3, name=building3_info[0], list=building3_info[1])
        await build3.create()
    except:
        print("Ошибка при создании таблиц зданий")


async def get_all_names():
    buildings = await Building.query.gino.all()
    names = []
    for e in buildings:
        names.append(e.name)
    return names


async def get_prices(name: str):
    building = await Building.query.where(name == Building.name).gino.first()
    return building.list
