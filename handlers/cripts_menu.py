import asyncio
import datetime
import random
from handlers import registration
import psycopg2 as sq
from aiogram import types, Dispatcher
from create_bot import dp,bot
from keyboards import admin_kb,client_kb,cripts_kb
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher.filters import Text



async def cripts_menu(message: types.Message):
    if registration.IsRegistration(message.from_user.id)==False:
        await message.answer('/reg - Вначале зарегистрируйтесь!')
        return
    global base, cur
    base = sq.connect(dbname='d9882ng2h7srs6', user='rixdvqeatezwpn',
                      password='60e4ac9ad7bcb8be1b8900f38fc0c70a52a69fb6dcdd59bf553c6262631f54a6', host='ec2-34-242-8-97.eu-west-1.compute.amazonaws.com')
    cur=base.cursor()
    cur.execute(f"SELECT * FROM cripts")
    json_valute={}
    for cripts_bd in cur.fetchall():
        json_valute[cripts_bd[0]]={
            'name':cripts_bd[1],
            'usd':cripts_bd[2],
            'chy':cripts_bd[3],
        }
    inform_text=(f'[~~~~~~Cripts~~~~~~]\n\n'
                 f'{json_valute["14"]["name"]} ₿-¥: {json_valute["14"]["chy"]}\n'
                 f'{json_valute["14"]["name"]} ₿-$: {json_valute["14"]["usd"]}\n\n'
                 f'{json_valute["15"]["name"]} Ξ-¥: {json_valute["15"]["chy"]}\n'
                 f'{json_valute["15"]["name"]} Ξ-$: {json_valute["15"]["usd"]}\n\n'
                 f'[~~~~~~~~~~~~~~~~]')
    await message.reply(f'{inform_text}',reply_markup=cripts_kb.kb_cripts_menu)



async def cripts_sell(message: types.Message):
    await message.reply(f'Продать:',reply_markup=cripts_kb.cripts_selection_sell)


    
async def cripts_buy(message: types.Message):
    await message.reply(f'Купить:',reply_markup=cripts_kb.cripts_selection_buy)



def register_handlers_cripts_list_menu(dp: Dispatcher):
    dp.register_message_handler(cripts_menu,commands=['cripts_menu','криптс_меню'])
    dp.register_message_handler(cripts_menu,Text(equals=['📈 сryptocurrency','📈 криптовалюта','📊 курс крипты']))
    dp.register_message_handler(cripts_sell,commands=['cripts_sell','крипту_продать'])
    dp.register_message_handler(cripts_sell,Text(equals=['📤 sell','📤 продать']))
    dp.register_message_handler(cripts_buy,commands=['cripts_buy','крипту_купить'])
    dp.register_message_handler(cripts_buy,Text(equals=['📥 buy','📥 купить']))
