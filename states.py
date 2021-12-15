from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    wait_for_add_manager = State()
    wait_for_delete_manager = State()
    wait_for_new_broadcast_message = State()
