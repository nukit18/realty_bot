import asyncio
import datetime

import aioschedule

from loader import bot, _
from utils.db_api import quick_commands_users, quick_commands_buildings, quick_commands_language


async def notification_payment_schedule():
    await asyncio.sleep(10)
    print("Запускаем скрипт рассылки об оплате")
    aioschedule.every().day.at("21:00").do(check_data_payment)  # 21:00
    print("Запускаем скрипт проверки просроченного платежа")
    aioschedule.every().day.at("09:00").do(late_payment)  # 09:00 делаем платеж просроченным
    aioschedule.every().day.at("09:30").do(update_payment_month)  # 09:30 обновляем всех пользователей на рассылку об оплате
    aioschedule.every().day.at("10:00").do(notification_late_payment)  # 10:00 рассылаем всем кто просрочил

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(60)


async def check_date_payment():
    return datetime.date.today().day == 1  # дата рассылки об оплате (1)


async def check_time_payment():
    return datetime.datetime.now().hour == 21  # время рассылки об оплате (21)


async def check_data_payment():
    if await check_date_payment() and await check_time_payment():
        print("Запускаю рассылку об оплате")
        try:
            await send_notification_payment()
        except:
            print("Произошла ошибка")
            return
        print("Рассылка прошла успешно")


async def send_notification_payment():
    students = await quick_commands_users.select_all_users()
    need_students = []
    for student in students:
        if student.payment_notification:
            need_students.append(student)
    for student in need_students:
        try:
            await asyncio.sleep(0.05)
            building = student.building
            room = student.room
            prices = await quick_commands_buildings.get_prices(building)
            price = 0
            for room_with_price in prices:
                if room_with_price[0] == room:
                    price = room_with_price[1]
            user = await bot.get_chat_member(student.id, student.id)
            await bot.send_message(student.id, _("Здравствуйте, {0}! Напоминаем, что сегодня необходимо внести оплату "
                                                 "проживания в размере {1} рублей.", locale=await quick_commands_language.get_language(student.id)).format(
                user.user.full_name, price))
        except:
            print(f"Произошла ошибка при отправке рассылке пользователю: {student.id}")


async def check_late_payment():
    return datetime.date.today().day == 2  # дата для выставления когда платеж начинает быть просроченным (2)


async def late_payment():
    if await check_late_payment():
        students = await quick_commands_users.select_all_users()
        for student in students:
            if student.payment_notification and not student.late_payment:
                await quick_commands_users.late_payment_true(student.id)


async def notification_late_payment():
    students = await quick_commands_users.select_all_users()
    for student in students:
        try:
            await asyncio.sleep(0.05)
            if student.payment_notification:
                if student.late_payment:
                    late_payment_days = (datetime.date.today() - datetime.timedelta(days=1)).day
                    building = student.building
                    room = student.room
                    prices = await quick_commands_buildings.get_prices(building)
                    price = 0
                    for room_with_price in prices:
                        if room_with_price[0] == room:
                            price = room_with_price[1]
                    user = await bot.get_chat_member(student.id, student.id)
                    if late_payment_days <= 5:
                        await bot.send_message(student.id,
                                               _("Здравствуйте, {0}! \n"
                                                 "Вам необходимо внести {1} и {2} рублей штраф за просроченный платеж.",
                                                 locale=await quick_commands_language.get_language(student.id)).format(
                                                   user.user.full_name, price, 100 * late_payment_days))
                    elif late_payment_days <= 10:
                        await bot.send_message(student.id,
                                               _("Здравствуйте, {0}! \n"
                                                 "Вам необходимо внести {1} и {2} рублей штраф за просроченный платеж.",
                                                 locale=await quick_commands_language.get_language(student.id)).format(
                                                   user.user.full_name, price, 300 * late_payment_days))
                    elif late_payment_days <= 20:
                        await bot.send_message(student.id,
                                               _("Здравствуйте, {0}! \n"
                                                 "Вам необходимо внести {1} и {2} рублей штраф за просроченный платеж.",
                                                 locale=await quick_commands_language.get_language(student.id)).format(
                                                   user.user.full_name, price, 500 * late_payment_days))
                    else:
                        continue
        except:
            print(f"Произошла ошибка при отправке рассылке пользователю: {student.id}")


async def update_payment_month_check_date():
    return datetime.date.today().day == 2  # дата для обновления информации (2)


async def update_payment_month():
    if await update_payment_month_check_date():
        students = await quick_commands_users.select_all_users()
        for student in students:
            await quick_commands_users.update_payment_notification(student.id)


