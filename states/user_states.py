from aiogram.dispatcher.filters.state import StatesGroup, State


class Download(StatesGroup):
    choice_platform = State()
    video_url = State()
