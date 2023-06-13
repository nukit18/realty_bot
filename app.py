from aiogram import executor

from handlers.users.end_visa_notification import end_visa_notification_schedule
from handlers.users.payment_notification import notification_payment_schedule
from loader import dp, db
import middlewares, filters, handlers
from utils.db_api import db_gino, quick_commands_buildings
from utils.notify_admins import on_startup_notify


async def on_startup(dispatcher):
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)
    print("Подключаем БД")
    await db_gino.on_startup(dp)
    print("Готово")
    dp.loop.create_task(notification_payment_schedule())
    dp.loop.create_task(end_visa_notification_schedule())

    print("Чистим БД")
    await db.gino.drop_all()
    print("Готово")

    print("Создаем таблицу")
    await db.gino.create_all()
    print("Готово")

    print("Создаем таблицу цен на команты")
    await quick_commands_buildings.create_db_buildings()
    print("Готово!")


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)


