# FSM - Finite State Machine
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot, ADMINS
from keyboards.client_kb import submit_markup, cancel_markup, direction_markup


class FSMAdmin(StatesGroup):
    name = State()
    id = State()
    direction = State()
    age = State()
    group = State()
    submit = State()


async def fsm_start(message: types.Message):
    if message.chat.type == 'private':
        if message.from_user.id in ADMINS:
            await FSMAdmin.name.set()
            await message.answer("Введите ваше Имя?",
                                 reply_markup=cancel_markup)
        else:
            await message.answer("ты нот мой админ!")
    else:
        await message.answer("Пиши в личку!")


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.from_user.id
        data['username'] = f"@{message.from_user.username}"
        data['name'] = message.text
    await FSMAdmin.next()
    await message.answer("Ваша id-шка?")


async def load_id(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['id'] = int(message.text)
        await FSMAdmin.next()
        await message.answer("Ваше направление?", reply_markup=direction_markup)
    except:
        await message.answer("Пиши нормально!")


async def load_direction(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['direction'] = message.text
    await FSMAdmin.next()
    await message.answer("Сколько вам лет?")


async def load_age(message: types.Message, state: FSMContext):
    try:
        if 16 < int(message.text) < 50:
            async with state.proxy() as data:
                data['age'] = int(message.text)
            await FSMAdmin.next()
            await message.answer("Какая группа?")
        else:
            await message.answer("Доступ воспрещен!")
    except:
        await message.answer("Пиши нормально!")


async def load_group(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['group'] = message.text
        await message.answer(f"{data['name']}\n{data['id']}\n{data['direction']}\n{data['age']}\n{data['username']}")
    await FSMAdmin.next()
    await message.answer("Все правильно?", reply_markup=submit_markup)


async def submit(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        # Запись в БД
        await state.finish()
        await message.answer("Все свободен!")
    elif message.text.lower() == "нет":
        await state.finish()
        await message.answer("Отмена")
    else:
        await message.answer("Нипонял!?")


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer("Отмена", reply_markup=submit_markup)


def register_handlers_fsm_anketa(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, state='*', commands=['cancel'])
    dp.register_message_handler(cancel_reg, Text(equals='cancel', ignore_case=True), state='*')

    dp.register_message_handler(fsm_start, commands=['reg'])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_id, state=FSMAdmin.id)
    dp.register_message_handler(load_direction, state=FSMAdmin.direction)
    dp.register_message_handler(load_age, state=FSMAdmin.age)
    dp.register_message_handler(load_group, state=FSMAdmin.group)
    dp.register_message_handler(submit, state=FSMAdmin.submit)
