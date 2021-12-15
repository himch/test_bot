import asyncio
from aiogram import types

from config import DEVELOPER_ID, ADMIN_ID
from dbase import all_managers, add_user
from misc import bot


async def get_user_data(data, message):
    data['db_tgid'] = message.from_user.id
    data['db_full_name'] = message.from_user.full_name
    await add_user(data['db_tgid'], message.chat.id)


async def print_user(tg_id):
    try:
        user = await bot.get_chat(tg_id)
    except Exception:
        return ('<a href="tg://user?id=' + str(tg_id) + '">' +
                "-- утрачен --</a>, id = " + str(tg_id))
    else:
        last_name = '' if user.last_name is None else ' ' + str(user.last_name)
        full_name = user.first_name + last_name
        return ('<a href="tg://user?id=' + str(tg_id) + '">' + full_name +
                "</a>, id = " + str(tg_id))


async def print_user_list(message, users, row_index):
    """Generate and print clickable Telegram user list."""
    if len(users) > 0:
        for row in users:
            await message.answer(await print_user(row[row_index]),
                                 reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("Нет таких, список пуст",
                             reply_markup=types.ReplyKeyboardRemove())


async def send_info_to_managers(bot, st, keyboard=None):
    managers = await all_managers()
    for manager in managers:
        try:
            await bot.send_message(manager[0], st, reply_markup=keyboard)
        except Exception:
            pass
        await asyncio.sleep(1)
    try:
        await bot.send_message(DEVELOPER_ID, st, reply_markup=keyboard)
    except Exception:
        pass
    await asyncio.sleep(1)


async def send_info_to_channel(bot, channel_id, info_to_send, keyboard=None):
    if isinstance(info_to_send, str):
        info_to_send = [info_to_send, ]
    for item in info_to_send:
        try:
            await bot.send_message(channel_id, str(item), reply_markup=keyboard)
        except Exception:
            pass
        await asyncio.sleep(1)


async def send_info_to_dev_admin(bot, st, keyboard=None):
    try:
        await bot.send_message(DEVELOPER_ID, st, reply_markup=keyboard)
    except Exception:
        pass
    try:
        if DEVELOPER_ID != ADMIN_ID:
            await bot.send_message(ADMIN_ID, st, reply_markup=keyboard)
    except Exception:
        pass
    await asyncio.sleep(1)
