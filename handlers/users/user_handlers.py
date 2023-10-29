import re

from urllib.parse import urlparse

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, CommandHelp, Command

from loader import dp, bot
from utils.download_videos import *
from utils.user_inline_keyboards import *
from states.user_states import *


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    bot_name = await dp.bot.get_me()
    user = message.from_user
    text = f'<b>{user.username}</b>, привет!\n\nЭто бот, с помощью которого можно скачивать видео с различных платформ 🖼' \
           f'\n\nОтправьте команду <b>/download</b>, чтобы скачать видео 💾\n<b>Максимальный размер видео 50MB!</b>'

    await message.answer(text)


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = "Доступные команды бота 📃:\n" \
           "/download - скачать видео"

    await message.answer(text)


@dp.message_handler(Command('download'))
async def get_video_platform(message: types.Message):
    await message.answer('<b>Выберите платформу, откуда вы хотите скачать видео 🖼:</b>',
                         reply_markup=inline_download_panel)
    await Download.first()


@dp.callback_query_handler(text_contains='platform', state=Download.choice_platform)
async def get_video_url(callback: types.CallbackQuery, state: FSMContext):
    platform = callback.data.split(':')[-1]

    async with state.proxy() as data:
        data['video_platform'] = platform

    await callback.message.edit_text('<b>Отправьте ссылку на видео 🔗:</b>')
    await Download.next()


@dp.message_handler(state=Download.video_url)
async def get_video_url(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['video_url'] = message.text
        data['video_platform_domain'] = urlparse(data['video_url'])
        video_data = None
        download_message = None
        video_url_correct = False

        if (data['video_platform'] == 'yt' and data['video_platform_domain'].netloc in ['www.youtube.com', 'youtu.be']) or \
                (data['video_platform'] == 'vk' and data['video_platform_domain'].netloc == 'vk.com'):
            download_message = await message.answer('<b>Видео загружается...</b>')
            video_data = download_yt_vk_video(data['video_url'])
            video_url_correct = True

        elif data['video_platform'] == 'zen' and data['video_platform_domain'].netloc == 'dzen.ru':
            download_message = await message.answer('<b>Видео загружается...</b>')
            video_data = download_zen_video(data['video_url'])
            video_url_correct = True

        else:
            await message.answer('<b>Введена некорректная ссылка на видео! Введите\nкоманду '
                                 '/download и повторите попытку</b>')
            await state.reset_data()
            await state.reset_state()

        if video_url_correct:
            video_path = rf"utils/videos/{video_data['file_name']}"

            with open(video_path, 'rb') as video:
                await message.answer_video(video, caption=video_data['video_name'])

            os.remove(video_path)

            await download_message.delete()
            await state.reset_data()
            await state.reset_state()


@dp.callback_query_handler(text='exit', state=Download.choice_platform)
async def exit_from_test(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.reset_data()
    await state.reset_state()


@dp.message_handler(Command('reset'), state='*')
async def state_reset(message: types.Message, state: FSMContext):
    await message.answer('<b>Состояния сброшены!</b>')
    await state.reset_data()
    await state.reset_state()
