import filters, middlewares, handlers
from aiogram import executor
from loader import dp
from utils import set_bot_commands


async def on_startup(dispatcher):
    await set_bot_commands.set_default_commands(dispatcher)

    print('Бот включен!')


async def on_shutdown(dispatcher):
    print('Бот выключен!')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)
