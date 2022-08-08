from aiogram import Dispatcher,types
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton, InlineKeyboardMarkup,InlineKeyboardButton



news_selection=InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton(text='Cybersports',callback_data='cybersports_news'),InlineKeyboardButton(text='Ixbt',callback_data='ixbt_news'))
news_cybersports_games_kolv=InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton(text='5 новостей',callback_data='5_newns_cybersports_games'),InlineKeyboardButton(text='All',callback_data='all_newns_cybersports_games'),InlineKeyboardButton(text='10 новостей',callback_data='10_newns_cybersports_games'))
news_ixbt_games_kolv=InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton(text='5 новостей',callback_data='5_newns_ixbt_games'),InlineKeyboardButton(text='All',callback_data='all_newns_ixbt_games'),InlineKeyboardButton(text='10 новостей',callback_data='10_newns_ixbt_games'))
