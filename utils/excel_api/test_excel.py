import asyncio

from utils.excel_api import excel_commands as ec


async def test():
    print("Получаем Маршала Жукова Имя")
    name1 = await ec.get_MJ()
    print(name1[0])
    print("Получаем Данные")
    info1 = await ec.get_MJ()
    print(info1[1])

    print("Получаем Переулок Автоматики Имя")
    name2 = await ec.get_PA()
    print(name2[0])
    print("Получаем Данные")
    info2 = await ec.get_PA()
    print(info2[1])

    print("Получаем Красноармейскую Имя")
    name3 = await ec.get_KA()
    print(name3[0])
    print("Получаем Данные")
    info3 = await ec.get_KA()
    print(info3[1])


loop = asyncio.get_event_loop()
loop.run_until_complete(test())