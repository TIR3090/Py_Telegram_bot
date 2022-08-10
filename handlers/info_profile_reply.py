import random
import requests
from aiogram import types, Dispatcher
from translate import Translator
from bs4 import BeautifulSoup
import asyncio
from create_bot import dp, bot
import psycopg2 as sq
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher.filters import Text
from handlers import registration
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton, InlineKeyboardMarkup,InlineKeyboardButton



async def info_reply(message: types.Message):
    global base, cur
    base = sq.connect(dbname='d9882ng2h7srs6',
                      user='rixdvqeatezwpn',
                      password='60e4ac9ad7bcb8be1b8900f38fc0c70a52a69fb6dcdd59bf553c6262631f54a6',
                      host='ec2-34-242-8-97.eu-west-1.compute.amazonaws.com')
    cur=base.cursor()
    if message.reply_to_message:
        cur.execute(f"SELECT * FROM profile WHERE id='{message.reply_to_message.from_user.id}'")
        for information in cur.fetchall():
            translate_p2p=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Перевести',callback_data=f'translate_p2p_{message.from_user.id}_{message.reply_to_message.from_user.id}'))
            await message.answer_photo(information[2],
                                       f'[~~~Профиль~~~]\n\n'
                                       f'🎫 id: {information[0]}\n'
                                       f'💻 Ник: {information[4]}\n'
                                       f'💴 ¥: {information[6]}\n'
                                       f'💵 $: {information[7]}\n\n'
                                       f'[=====-Cripts-=====]\n\n'
                                       f'💼 ₿-¥: {"{:0.9f}".format(information[10])}\n'
                                       f'💼 ₿-$: {"{:0.9f}".format(information[8])}\n\n'
                                       f'💼 Ξ-¥: {"{:0.9f}".format(information[14])}\n'
                                       f'💼 Ξ-$: {"{:0.9f}".format(information[12])}\n\n'
                                       f'[~~~~~~~~~~~~~]',reply_markup=translate_p2p)
    else:
        cur.execute(f"SELECT * FROM profile WHERE id='{message.from_user.id}'")
        for information in cur.fetchall():
            await message.answer_photo(information[2],
                                       f'[~~~Профиль~~~]\n\n'
                                       f'🎫 id: {information[0]}\n'
                                       f'💻 Ник: {information[4]}\n'
                                       f'💴 ¥: {information[7]}\n'
                                       f'💵 $: {information[6]}\n\n'
                                       f'[=====-Cripts-=====]\n\n'
                                       f'💼 ₿-¥: {"{:0.9f}".format(information[10])}\n'
                                       f'💼 ₿-$: {"{:0.9f}".format(information[8])}\n\n'
                                       f'💼 Ξ-¥: {"{:0.9f}".format(information[14])}\n'
                                       f'💼 Ξ-$: {"{:0.9f}".format(information[12])}\n\n'
                                       f'[~~~~~~~~~~~~~]')


async def p2p_usd_chy(callback: types.CallbackQuery):
    from_p2p=callback.data.split('_')[2]
    for_p2p=callback.data.split('_')[3]
    if callback.from_user.id == int(from_p2p):
            translate_p2p_selected=InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Chy-¥',callback_data=f'chy_translate_p2p_{from_p2p}_{for_p2p}'),InlineKeyboardButton(text='Usd-$',callback_data=f'usd_translate_p2p_{from_p2p}_{for_p2p}'))
            await callback.message.edit_reply_markup(reply_markup=translate_p2p_selected)
    else:
        await callback.answer(text='Не вы начали перевод!', show_alert=True)



def register_handlers_info_reply(dp: Dispatcher):
    dp.register_message_handler(info_reply, commands=['info','инфо'])
    dp.register_callback_query_handler(p2p_usd_chy,lambda callback: callback.data.startswith('translate_p2p_'))
