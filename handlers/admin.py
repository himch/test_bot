from aiogram import types
from aiogram.dispatcher import FSMContext

from dbase import user_is_admin, all_managers, add_manager, delete_manager, all_users, delete_all_users
from misc import dp, bot
from states import States
from utils import print_user_list



#######################################################################################################################
# admin commands
#######################################################################################################################
@dp.message_handler(commands="admin", state="*")
async def cmd_admin(message: types.Message, state: FSMContext):
    if await user_is_admin(message.from_user.id):
        await message.answer("Список команд для админа:\n" +
                             "/addmanager - добавить менеджера\n" +
                             "/deletemanager - удалить менеджера\n" +
                             "/allmanagers - список всех менеджеров\n\n" +
                             "/newbroadcastmessage - разослать сообщения\n\n" +
                             "/allusers - список всех пользователей\n" +
                             "/deleteallusers - удалить всех пользователей\n\n",
                             reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("Вас нет в списке администраторов. Обратитесь в техническую поддержку",
                             reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands="allmanagers", state="*")
async def cmd_all_managers(message: types.Message, state: FSMContext):
    if await user_is_admin(message.from_user.id):
        await message.answer("Список менеджеров:",
                             reply_markup=types.ReplyKeyboardRemove())
        await print_user_list(message, await all_managers(), 0)
        await message.answer("Нажмите /admin для списка команд админа", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(None)
    else:
        await message.answer("Вас нет в списке администраторов. Обратитесь в техническую поддержку",
                             reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands="addmanager", state="*")
async def cmd_add_manager(message: types.Message, state: FSMContext):
    if await user_is_admin(message.from_user.id):
        await message.answer("Перешлите сюда сообщение от пользователя, которого вы хотите назначить менеджером "
                             "или нажмите /cancel для отмены",
                             reply_markup=types.ReplyKeyboardRemove())
        await States.wait_for_add_manager.set()
    else:
        await message.answer("Вас нет в списке администраторов. Обратитесь в техническую поддержку",
                             reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=States.wait_for_add_manager, content_types=types.ContentTypes.ANY)
async def add_manager_step2(message: types.Message, state: FSMContext):
    if message.text.isdecimal():
        await add_manager(int(message.text))
        await message.answer("Добавлен id = " + message.text,
                             reply_markup=types.ReplyKeyboardRemove())
    else:
        if message.forward_from is None:
            tgid = message.from_user.id
            full_name = message.from_user.full_name
        else:
            tgid = message.forward_from.id
            full_name = message.forward_from.full_name
        await add_manager(tgid)
        await message.answer("Добавлен(а) " + full_name + ", id = " + str(tgid),
                             reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(None)


@dp.message_handler(commands="deletemanager", state="*")
async def cmd_delete_manager(message: types.Message, state: FSMContext):
    if await user_is_admin(message.from_user.id):
        await message.answer(
            "Перешлите сюда сообщение от пользователя, которого вы хотите удалить из списка менеджеров или нажмите /cancel для отмены",
            reply_markup=types.ReplyKeyboardRemove())
        await States.wait_for_delete_manager.set()
    else:
        await message.answer("Вас нет в списке администраторов. Обратитесь в техническую поддержку",
                             reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=States.wait_for_delete_manager, content_types=types.ContentTypes.ANY)
async def delete_manager_step2(message: types.Message, state: FSMContext):
    if message.forward_from is None:
        tgid = message.from_user.id
        full_name = message.from_user.full_name
    else:
        tgid = message.forward_from.id
        full_name = message.forward_from.full_name
    await delete_manager(tgid)
    await message.answer("Удален(а) " + full_name + ", id = " + str(tgid),
                         reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(None)


@dp.message_handler(commands="allusers", state="*")
async def cmd_all_users(message: types.Message, state: FSMContext):
    if await user_is_admin(message.from_user.id):
        await message.answer("Список пользователей:",
                             reply_markup=types.ReplyKeyboardRemove())
        await print_user_list(message, await all_users(), 0)
        await message.answer("Нажмите /admin для списка команд админа", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(None)
    else:
        await message.answer("Вас нет в списке администраторов. Обратитесь в техническую поддержку",
                             reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands="deleteallusers", state="*")
async def cmd_delete_all_users(message: types.Message, state: FSMContext):
    if await user_is_admin(message.from_user.id):
        await delete_all_users()
        await message.answer("Готово", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(None)
    else:
        await message.answer("Вас нет в списке администраторов. Обратитесь в техническую поддержку",
                             reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands="newbroadcastmessage", state="*")
async def cmd_new_broadcast_message(message: types.Message, state: FSMContext):
    if await user_is_admin(message.from_user.id):
        await message.answer("Введите новое сообщение (имя пользователя вставь как [user])  или нажмите /cancel для отмены:",
                             reply_markup=types.ReplyKeyboardRemove())
        await States.wait_for_new_broadcast_message.set()
    else:
        await message.answer("Вас нет в списке администраторов. Обратитесь в техническую поддержку",
                             reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=States.wait_for_new_broadcast_message, content_types=types.ContentTypes.ANY)
async def new_broadcast_message_step2(message: types.Message, state: FSMContext):
    users = await all_users()
    for user in users:
        chat = await bot.get_chat(user[1])
        st = message.text.replace("[user]", chat.username)
        await bot.send_message(user[1], st)
    await message.answer("Готово", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(None)

