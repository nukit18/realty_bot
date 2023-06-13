import asyncio
import datetime

import aioschedule

from loader import bot, _
from utils.db_api import quick_commands_users, quick_commands_language


async def end_visa_notification_schedule():
    await asyncio.sleep(10)
    print("Запускаем скрипт отправки уведомлений по визе")
    aioschedule.every().day.at("10:00").do(notify_end_days)  #
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(59)


async def notify_end_days():
    students = await quick_commands_users.select_all_users()
    for student in students:
        try:
            if student.visa_requirement:
                delta_days = (student.end_visa - datetime.date.today()).days
                if delta_days == 41:
                    await bot.send_message(student.id,
                                           _("Ваша виза заканчивается через 40 дней. Пожалуйста, принесите новую визу администратору после ее получения. Мы сделаем вам новую регистрацию.",
                                             locale=await quick_commands_language.get_language(student.id)))
                    continue
                if delta_days == 11:
                    await bot.send_message(student.id,
                                           _("Ваша виза заканчивается через 10 дней. Пожалуйста, принесите новую визу администратору после ее получения. "
                                             "Мы сделаем вам новую регистрацию.", locale=await quick_commands_language.get_language(student.id)))
                    continue
                if delta_days == 1:
                    await bot.send_message(student.id,
                                           _("Ваша виза заканчивается завтра. Пожалуйста, принесите новую визу администратору после ее получения. "
                                             "Мы сделаем вам новую регистрацию.", locale=await quick_commands_language.get_language(student.id)))
                    continue
                if delta_days <= 0:
                    await bot.send_message(student.id,
                                           _("Срочно! Срок действия вашей визы истёк! Регистрация закончилась! "
                                             "Принесите новую визу, чтобы мы могли сделать вам регистрацию.",
                                             locale=await quick_commands_language.get_language(student.id)))

        except:
            print(f"Произошла ошибка при отправке рассылке пользователю: {student.id}")
