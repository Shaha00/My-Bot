from aiogram import Dispatcher, types
from config import bot, ADMINS


async def ban(message: types.Message):
    if message.chat.type == "group":
        if message.from_user.id not in ADMINS:
            await message.answer("Ты не мой босс!")
        elif not message.reply_to_message:
            await message.answer("Команда должна быть ответом на сообщение!")
        else:
            await bot.kick_chat_member(message.chat.id,
                                       message.reply_to_message.from_user.id)
            await message.answer(f'{message.from_user.first_name} братан кикнул '
                                 f'{message.reply_to_message.from_user.full_name}')
    else:
        await message.answer("Пиши в группе!")


async def pin(message: types.Message):
    if message.chat.type == "supergroup":
        if message.from_user.id not in ADMINS:
            await message.answer("Закреплять может только админ!")
        else:
            await bot.pin_chat_message(message.chat.id,
                                       message.message_id,
                                       message.reply_to_message)
    # else:
    #     await message.answer("Закрепляй  в группе")


async def dice(message: types.Message):
    a = await bot.send_dice(message.from_user.id, emoji='🎲')
    b = await bot.send_dice(message.from_user.id, emoji='🎲')
    if a.dice.value > b.dice.value:
        await bot.send_message(message.from_user.id, "Bot winner!")
    elif a.dice.value == b.dice.value:
        await bot.send_message(message.from_user.id, "Ничья!")
    else:
        await bot.send_message(message.from_user.id, "You win!")


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(ban, commands=['ban'], commands_prefix='!/')
    dp.register_message_handler(pin, commands=['pin'], commands_prefix='!/')
    dp.register_message_handler(dice, commands=['dice'], commands_prefix='!/')
