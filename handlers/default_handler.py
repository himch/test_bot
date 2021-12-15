from misc import dp
from aiogram import types


#####################################################################################################################
# default
@dp.message_handler(content_types=types.ContentTypes.ANY, state="*")
async def all_other_messages(message: types.Message):
    """Default handler"""
    if message.content_type == "text":
        await message.reply("Ничего не понимаю!")
    else:
        await message.reply("Я не умею обрабатывать " + message.content_type + "!")