import aioschedule
from aiogram import types, Dispatcher
from config import bot
import asyncio


async def get_chat_id(message: types.Message):
    global chat_id
    chat_id = message.from_user.id
    await message.answer('Окак')


async def to_lesson():
    await bot.send_message(chat_id=chat_id, text="Сегодня урок кирвесен нб поставлю")


async def wake_up():
    photo = open('media/028df0020a0f184e0fc08cb4c84b47a3.jpg', 'rb')
    await bot.send_photo(chat_id=chat_id, photo=photo,
                         caption="Доброе утро, держи мемчик с утречка!")


async def not01():
    aioschedule.every().friday.at('18:00').do(to_lesson)
    aioschedule.every().day.at('07:30').do(wake_up)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(2)


def register_handlers_schedule(dp: Dispatcher):
    dp.register_message_handler(get_chat_id,
                                lambda word: 'напомни' in word.text)
