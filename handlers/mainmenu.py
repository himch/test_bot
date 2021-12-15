from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from datetime import datetime
from pydub import AudioSegment

from config import ADMIN_ID
from dbase import add_media
from face_recognizer import get_faces_images
from keyboards import main_menu_keyboard, search_btn, last5_btn, all_btn, next_btn, about_btn
from media import search, print_search_result
from messages import messages
from misc import dp, bot
from utils import get_user_data, print_user, send_info_to_managers


#######################################################################################################################
# general commands
#######################################################################################################################

@dp.message_handler(commands="start", state="*")
@dp.message_handler(Text(equals="старт", ignore_case=True), state="*")
async def cmd_start(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await get_user_data(data, message)
        media = types.InputFile('start_pic.jpg')
        await message.answer_photo(media, reply_markup=main_menu_keyboard)
        await message.answer(messages["start_message"].replace("[user]", message.from_user.username),
                             reply_markup=main_menu_keyboard)

        await send_info_to_managers(bot, "Новый пользователь " + await print_user(data['db_tgid']))
        await state.set_state(None)


@dp.message_handler(commands="about", state="*")
@dp.message_handler(Text(startswith=about_btn, ignore_case=True), state="*")
async def cmd_about(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await get_user_data(data, message)
        await message.answer(messages["about_message"].replace("[user]", message.from_user.username)
                             + await print_user(ADMIN_ID),
                             reply_markup=main_menu_keyboard)
        await state.set_state(None)


# Обработка присланной картинки
@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await get_user_data(data, message)
        now = str(datetime.now()).translate(str.maketrans({' ': '_', ':': '-', '.': '_'}))
        image_filename = "files/" + now + ".jpg"
        await message.photo[-1].download(image_filename)
        faces_images = await get_faces_images(image_filename)

        if len(faces_images) > 0:
            await add_media(data['db_tgid'], image_filename, 'image')
            st = "👌 Картинка сохранена в БД пользователя " + str(data['db_tgid'])
        else:
            st = "Лица ищутся методом каскадов Хаара, будь снисходителен на случай ошибки, по-братски, а?\n\n" \
                 "😞 Картинка не сохранена"

        await message.answer("Обнаружено лиц: " + str(len(faces_images)) + "\n\n" + st)
        await state.set_state(None)


# Обработка присланного голосового
@dp.message_handler(content_types=['voice'])
async def handle_docs_voice(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await get_user_data(data, message)
        now = str(datetime.now()).translate(str.maketrans({' ': '_', ':': '-', '.': '_'}))
        ogg_voice_filename = "files/" + now + ".ogg"
        wav_voice_filename = "files/" + now + ".wav"

        voice = await message.voice.get_file()
        await bot.download_file(voice.file_path, ogg_voice_filename)

        sound = AudioSegment.from_ogg(ogg_voice_filename)
        sound = sound.set_frame_rate(16000)
        sound.export(wav_voice_filename, format="wav")

        await add_media(data['db_tgid'], wav_voice_filename, 'voice')
        await message.answer_document(types.InputFile(wav_voice_filename),
                                      caption="👌 Конвертированное голосовое в формате wav 16kHz "
                                              "сохранено в БД пользователя " + str(data['db_tgid']))
        await state.set_state(None)


# Последние 5
@dp.message_handler(commands=['last5'], state="*")
@dp.message_handler(Text(startswith=last5_btn, ignore_case=True), state="*")
async def cmd_last5(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await get_user_data(data, message)
        data["offset"] = 0
        await search(data, message, method="last5", offset=data["offset"])
        await print_search_result(data, message, method="last5")


# Следующие
@dp.message_handler(commands=['next'], state="*")
@dp.message_handler(Text(startswith=next_btn, ignore_case=True), state="*")
async def cmd_next(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await get_user_data(data, message)
        if "offset" in data:
            data["offset"] += 5
        else:
            data["offset"] = 0
        await search(data, message, method="last5", offset=data["offset"])
        await print_search_result(data, message, method="last5")


# Все
@dp.message_handler(commands=['all'], state="*")
@dp.message_handler(Text(startswith=all_btn, ignore_case=True), state="*")
async def cmd_all(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await get_user_data(data, message)
        await search(data, message, method="all")
        await print_search_result(data, message, method="all")


# Поиск подсказка
@dp.message_handler(commands=['search'], state="*")
@dp.message_handler(Text(startswith=search_btn, ignore_case=True), state="*")
async def cmd_search(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await get_user_data(data, message)
        await message.answer("🔎 Для поиска по базе данных введи ID пользователя",
                             reply_markup=main_menu_keyboard)


# Поиск
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def line_search(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await get_user_data(data, message)
        await search(data, message, method="search")
        await print_search_result(data, message, method="search")
        await state.set_state(None)


#####################################################################################################################
# Отмена
@dp.message_handler(commands=['cancel'], state="*")
# @dp.message_handler(Text(startswith=cancel_btn, ignore_case=True), state="*")
async def cancel_cmd(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await message.answer("Отменено")
        await state.set_state(None)
