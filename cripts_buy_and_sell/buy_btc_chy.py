﻿import asyncio
import keyboards
from handlers import registration
# import psycopg2 as sq
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher.filters import Text
from create_bot import dp, bot
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton, InlineKeyboardMarkup,InlineKeyboardButton
import aiosqlite as aoisq




class FSMbuybitcoin_chy(StatesGroup):
    summa=State()
    delet_msg=State()
    chat_id=State()


async def start_buy_chy(callback: types.CallbackQuery,state: FSMContext):
    await callback.message.delete()
    if await registration.IsRegistration(callback.from_user.id)==False:
        await callback.message.answer('/reg - Вначале зарегистрируйтесь!')
        return
    cancel_handler_cripts_buy=InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton(text='Отмена',callback_data=f'cancel_state_cripts_buy_{callback.from_user.id}'))
    msg = await callback.message.answer('Введите сумму:',reply_markup=cancel_handler_cripts_buy)
    async with state.proxy() as data:
        data['delet_msg']=msg.message_id
        data['chat_id']=msg.chat.id
    await FSMbuybitcoin_chy.summa.set()
    await asyncio.sleep(120)
    current_state=await state.get_state()
    if current_state is None:
        return
    await bot.delete_message(chat_id=msg.chat.id,message_id=msg.message_id)
    await state.finish()
    await callback.message.answer('Время ожидания вышло!')



async def buy_btc_chy(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['summa']=message.text
    summa_preor=await state.get_data()
    summa_preor_btc=summa_preor.get('summa')
    msg_id=summa_preor.get('delet_msg')
    chat_id=summa_preor.get('chat_id')
    if summa_preor_btc.replace('.','',1).isdigit() or summa_preor_btc.replace(',','',1).isdigit() :
        if await registration.IsRegistration(message.from_user.id)==False:
            await message.answer('/reg - Вначале зарегистрируйтесь!')
            return
        global base, cur
        # base = sq.connect(dbname='d9882ng2h7srs6',
        #                   user='rixdvqeatezwpn',
        #                   password='60e4ac9ad7bcb8be1b8900f38fc0c70a52a69fb6dcdd59bf553c6262631f54a6',
        #                   host='ec2-34-242-8-97.eu-west-1.compute.amazonaws.com')
        # cur=base.cursor()
        base =await aoisq.connect("data_base/data_casino_keeper.db")
        cur=await base.cursor()
        await cur.execute(f"SELECT * FROM cripts")
        json_valute={}
        for cripts_bd in await cur.fetchall():
            json_valute[cripts_bd[0]]={
                'name':cripts_bd[1],
                'usd':cripts_bd[2],
                'chy':cripts_bd[3],
            }
        await cur.execute(f"SELECT * FROM profile WHERE id='{message.from_user.id}'")
        for data_bd in await cur.fetchall():
            balance_chy=data_bd[7]
            btc_chy_na_chetu=data_bd[10]
            nickname=data_bd[4]
        if float(summa_preor_btc.replace(',','.'))<=0:
            await message.answer('Сумма 0 !?')
            return
        elif balance_chy<float(summa_preor_btc.replace(',','.')):
            await message.answer('❌ Недостаточно chy!')
            return
        kol_btc_buy_pol=float(summa_preor_btc)/json_valute['14']['chy']
        kol_btc_buy=btc_chy_na_chetu+kol_btc_buy_pol
        balance_chy_v_bd_write=balance_chy-float(summa_preor_btc)
        await cur.execute(f"UPDATE profile SET balance_chy={round(balance_chy_v_bd_write,3)},btc_chy={round(kol_btc_buy,9)},price_buy_btc_chy={json_valute['14']['chy']} WHERE id='{message.from_user.id}'")
        await base.commit()
        await message.delete()
        await message.answer(f"✅ {nickname} приобрел:\nBTC в ¥: {'{:0.9f}'.format(kol_btc_buy_pol)}\nЗа: {summa_preor_btc} ¥")
        await bot.delete_message(chat_id=chat_id,message_id=msg_id)
        await state.finish()
    else:
        await message.answer('Некорректная сумма!')
        return



def register_handlers_buy_btc_chy(dp: Dispatcher):
    dp.register_callback_query_handler(start_buy_chy,text='bitcoin_valuta_chy_buy',state=None)
    dp.register_message_handler(buy_btc_chy,state=FSMbuybitcoin_chy.summa)
