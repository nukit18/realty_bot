import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS
from keyboards.default.change_date_visa import new_visa_func
from keyboards.inline.cancel_keyboard import cancel_keyboard_func
from keyboards.inline.confirm_personal_data import confirm_personal_keyboard_func
from keyboards.inline.keyboard_buildings import buildings_keyboard_func
from keyboards.inline.keyboard_citizenship import citizenship_keyboard_func
from keyboards.inline.keyboard_rooms import rooms_keyboard
from keyboards.inline.language_keyboard import language_keyboard
from keyboards.inline.write_to_us import write_us_keyboard_func
from loader import dp, bot, _
from utils.db_api import quick_commands_users, quick_commands_language


async def check_visa(date_str):
    try:
        date = datetime.datetime.strptime(date_str, "%Y.%m.%d").date()
    except:
        return False
    now = datetime.datetime.now().date()
    if date < now:
        return False
    return True


@dp.callback_query_handler(text="cancel", state=["new_visa_input", "input_fullname", "input_citizenship", "input_visa",
                                                 "input_country", "input_room", "finish"])
async def cancel(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await bot.send_message(call.from_user.id, _("Вы отменили ввод!"))
    await state.reset_data()
    await state.finish()


@dp.message_handler(CommandStart())
async def choice_language(message: types.Message):
    user_id = message.from_user.id
    if str(user_id) in ADMINS:
        await message.answer("Привет, {0}! "
                             "Вы являетесь администратором.\n"
                             "Список доступных команд - /help".format(message.from_user.full_name))
        return
    await message.answer(_("Выберите язык:"), reply_markup=language_keyboard)


@dp.callback_query_handler(text=["lang_en", "lang_ru"])
async def bot_start(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    if str(user_id) in ADMINS:
        await call.message.answer((f"Привет, {call.from_user.full_name}! "
                                   f"Вы являетесь администратором.\n"
                                   f"Список доступных команд - /help"))
        return

    lang = call.data[5:]
    try:
        await quick_commands_language.update_language(user_id, lang)
    except:
        await quick_commands_language.add_user(user_id, lang)
    users_id = await quick_commands_users.get_ids()
    if (user_id,) in users_id:
        student = await quick_commands_users.select_user(user_id)
        if student.citizenship == "Дальнее":
            input_new_visa = await new_visa_func()
            await bot.send_message(user_id, ((_("Привет, {0}!\n"
                                                "Вы уже зарегистрированы!",
                                                locale=lang)).format(call.from_user.full_name)),
                                   reply_markup=input_new_visa)
        else:

            await bot.send_message(user_id, (_("Привет, {0}!\n"
                                               "Вы уже зарегистрированы!", locale=lang)).format(
                call.from_user.full_name))
        return
    confirm_personal_keyboard = await confirm_personal_keyboard_func(lang)
    await bot.send_message(user_id, (_("Привет, {0}!\n"
                                       "Я бот для студентов, проживающих в частных общежитиях. "
                                       "С моей помощью вы получите важные уведомления и сможете быстро получить ответ на свой вопрос. "
                                       "Чтобы начать, нужно зарегистрироваться. Вы согласны с обработкой персональных данных?",
                                       locale=lang)).format(call.from_user.full_name),
                           reply_markup=confirm_personal_keyboard)


@dp.callback_query_handler(text="personal_yes")
async def personal_yes(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    cancel_keyboard = await cancel_keyboard_func()
    await bot.send_message(user_id, _("Введите ФИО:"), reply_markup=cancel_keyboard)
    await state.set_state("input_fullname")


@dp.callback_query_handler(text="personal_no")
async def personal_no(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    await state.reset_data()
    await state.finish()
    await bot.send_message(user_id, _("Извините, тогда вы не можете мной пользоваться."))


@dp.message_handler(text="Ввести новую визу.")
async def change_visa(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if str(user_id) in ADMINS:
        return
    student = await quick_commands_users.select_user(user_id)
    if student.citizenship == "Ближнее":
        await message.answer(_("Вы выбрали ближнее зарубежье, виза не нужна."))
        return
    if student.visa_requirement:
        await message.answer(_("Сначала сообщите о новой визе администратору."))
        return
    cancel_keyboard = await cancel_keyboard_func()
    await message.answer(_("Введите, пожалуйста, дату окончания визы в формате ГГГГ.ММ.ДД:"),
                         reply_markup=cancel_keyboard)
    await state.set_state("new_visa_input")


@dp.message_handler(state="new_visa_input")
async def new_visa(message: types.Message, state: FSMContext):
    if not await check_visa(message.text):
        await message.answer(_("Пожалуйста, проверьте правильность написания.\nФормат: ГГГГ.ММ.ДД"))
        return
    await quick_commands_users.change_visa_date(message.from_user.id, message.text)
    await state.reset_data()
    await state.finish()
    await message.answer(_("Спасибо, данные изменены!"))


@dp.message_handler(state="input_fullname")
async def input_fullname(message: types.Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    citizenship_keyboard = await citizenship_keyboard_func()
    await message.answer(_("Выберите гражданство:"), reply_markup=citizenship_keyboard)
    await state.set_state("input_citizenship")


@dp.callback_query_handler(text="Ближнее", state="input_citizenship")
async def input_citizenship_near(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await state.update_data(citizenship=call.data)
    await bot.send_message(call.from_user.id, _("Расскажите, из какой вы страны:"))
    await state.set_state("input_country")


@dp.callback_query_handler(text="Дальнее", state="input_citizenship")
async def input_citizenship_distant(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await state.update_data(citizenship=call.data)
    await bot.send_message(call.from_user.id, _("Введите, пожалуйста, дату окончания визы в формате ГГГГ.ММ.ДД:"))
    await state.set_state("input_visa")


@dp.message_handler(state="input_visa")
async def input_visa(message: types.Message, state: FSMContext):
    date = message.text
    if not await check_visa(date):
        await message.answer(_("Пожалуйста, проверьте правильность написания.\nФормат: ГГГГ.ММ.ДД"))
        return
    await state.update_data(end_visa=date)
    await message.answer(_("Расскажите, из какой вы страны:"))
    await state.set_state("input_country")


@dp.message_handler(state="input_country")
async def input_country(message: types.Message, state: FSMContext):
    await state.update_data(country=message.text)
    keyboard = await buildings_keyboard_func()
    await message.answer(_("В каком из частных общежитий вы проживаете?"), reply_markup=keyboard)
    await state.set_state("input_room")


@dp.callback_query_handler(state="input_room")
async def input_room(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    building = call.data
    await state.update_data(building=building)
    keyboard = await rooms_keyboard(building)
    await call.message.answer(_("Выберите номер вашей комнаты:"), reply_markup=keyboard)
    await state.set_state("finish")


@dp.callback_query_handler(state="finish")
async def finish(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()
    end_visa = data.get("end_visa")
    if end_visa is None:
        await quick_commands_users.add_user(id=call.from_user.id, fullname=data.get("fullname"),
                                            citizenship=data.get("citizenship"),
                                            country=data.get("country"), building=data.get("building"),
                                            room=int(call.data))
    else:
        await quick_commands_users.add_user(id=call.from_user.id, fullname=data.get("fullname"),
                                            citizenship=data.get("citizenship"),
                                            country=data.get("country"), building=data.get("building"),
                                            room=int(call.data), end_visa=end_visa, visa_requirement=True)
    await state.reset_data()
    await state.finish()
    write_us_keyboard = await write_us_keyboard_func()
    await call.message.answer(_("Спасибо! Регистрация прошла успешно. {0}, мы рады, что вы с нами!\n"
                              "Если у вас возникнут вопросы, всегда можете написать нам.").format(call.from_user.full_name),
                              reply_markup=write_us_keyboard)
