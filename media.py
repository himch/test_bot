import asyncio
from aiogram import types
from config import MAX_SHOWED_MEDIA
from dbase import search_media
from misc import bot
from utils import print_user, send_info_to_dev_admin


async def search(data, message, method="search", offset=0):
    st = await print_user(data['db_tgid'])
    st = "Новый поиск пользователя " + st + ": " + message.text
    await send_info_to_dev_admin(bot, st)

    search_string = message.text.strip().upper()
    data['media'] = await search_media(search_string, method, offset)


async def print_search_result(data, message, method="search"):
    medias = data['media']
    medias_qnty = len(medias)

    medias = medias[:MAX_SHOWED_MEDIA]

    if medias_qnty == 0:
        await message.answer("Ничего не найдено.")
    else:
        for media in medias:
            media_file = types.InputFile(media['file_name'])
            st = media['media_type'].capitalize() + ", user " + await print_user(media['tgid'])
            if media['media_type'] == 'image':
                await message.answer_photo(media_file, caption=st)
            elif media['media_type'] == 'voice':
                await message.answer_document(media_file, caption=st)
            await asyncio.sleep(1)

        if method == "last5":
            await message.answer(f"Показаны с <b>{data['offset'] + 1}</b> "
                                 f"по <b>{data['offset'] + 5}\n</b>"
                                 f"Нажми /next чтобы вывести следующие 5")
        if method == "search" or method == "all":
            await message.answer("Всего найдено медиафайлов: <b>" + str(medias_qnty) + "</b>")
            if medias_qnty > MAX_SHOWED_MEDIA:
                await message.answer(f"Показаны первые {MAX_SHOWED_MEDIA}, "
                                     f"не стоит увеличивать энтропию и нервировать Telegram")
