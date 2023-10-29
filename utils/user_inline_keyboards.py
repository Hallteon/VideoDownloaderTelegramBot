from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

platform_callback_data = CallbackData('platform', 'name')

inline_download_panel = InlineKeyboardMarkup(row_width=2)
inline_download_panel.add(InlineKeyboardButton(text='Ютуб (видео / шортс)',
                                               callback_data=platform_callback_data.new(name='yt')),
                          InlineKeyboardButton(text='ВК (видео / клип)',
                                               callback_data=platform_callback_data.new(name='vk')),
                          InlineKeyboardButton(text='Дзен (видео)',
                                               callback_data=platform_callback_data.new(name='zen')))
inline_download_panel.add(InlineKeyboardButton(text='Выйти', callback_data='exit'))