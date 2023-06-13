from aiogram.dispatcher.filters.state import StatesGroup,State


class CheckPlace(StatesGroup):
    label = State()
    name = State()
    search = State()