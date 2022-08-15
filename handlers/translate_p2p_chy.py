import random
import requests
from aiogram import types, Dispatcher
from translate import Translator
from bs4 import BeautifulSoup
import asyncio
from create_bot import dp, bot
# import psycopg2 as sq
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher.filters import Text
from handlers import registration
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton, InlineKeyboardMarkup,InlineKeyboardButton
import aiosqlite as aoisq



class FSMtranslate_p2p_chy(StatesGroup):
    p2p=State()
    from_p2p=State()
    for_p2p=State()
    delet_msg=State()
    chat_id=State()



async  def cancel_handler_translate_p2p_chy(callback: types.CallbackQuery,state:FSMContext):
    translate_p2p_cancel=callback.data.split('_')[3]
    if callback.from_user.id == int(translate_p2p_cancel):
        await callback.message.delete()
        current_state=await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await callback.message.answer('Отмена перевода!')
    else:
        await callback.answer(text='Не твое сообщени!', show_alert=True)


async def Start_translate_p2p_chy(callback: types.CallbackQuery,state: FSMContext):
    await callback.message.delete()
    global base, cur
    # base = sq.connect(dbname='d9882ng2h7srs6',
    #                   user='rixdvqeatezwpn',
    #                   password='60e4ac9ad7bcb8be1b8900f38fc0c70a52a69fb6dcdd59bf553c6262631f54a6',
    #                   host='ec2-34-242-8-97.eu-west-1.compute.amazonaws.com')
    # cur=base.cursor()
    base =await aoisq.connect("data_base/data_casino_keeper.db")
    cur=await base.cursor()
    await cur.execute(f"SELECT * FROM profile WHERE id ='{callback.data.split('_')[3]}'")
    for info_bd in await cur.fetchall():
        nick=info_bd[4]
        balance_chy_chet=info_bd[7]
    inform_text=f'<b>{nick}</b> на счету:\n' \
                f'💴: {balance_chy_chet} ¥\n\n' \
                f'Сумма перевода:'
    translate_p2p_cancel=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Отмена',callback_data=f'translate_chy_cancel_{callback.from_user.id}'))
    msg = await callback.message.answer(text=inform_text,reply_markup=translate_p2p_cancel)
    async with state.proxy() as data:
        data['delet_msg']=msg.message_id
        data['chat_id']=msg.chat.id
        data['from_p2p']=callback.data.split('_')[3]
        data['for_p2p']=callback.data.split('_')[4]
    await FSMtranslate_p2p_chy.p2p.set()
    await asyncio.sleep(120)
    current_state=await state.get_state()
    if current_state is None:
        return
    await bot.delete_message(chat_id=msg.chat.id,message_id=msg.message_id)
    await state.finish()
    await callback.message.answer('Время ожидания вышло!')




async def translate_p2p_chy(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['p2p']=message.text
    p2p_get=await state.get_data()
    p2p=p2p_get.get('p2p')
    msg_id=p2p_get.get('delet_msg')
    chat_id=p2p_get.get('chat_id')
    from_p2p=p2p_get.get('from_p2p')
    for_p2p=p2p_get.get('for_p2p')
    if await registration.IsRegistration(message.from_user.id)==False:
        await message.answer('/reg - Вначале зарегистрируйтесь!')
        return
    await cur.execute(f"SELECT * FROM profile")
    json_info={}
    for info_bd in await cur.fetchall():
        json_info[info_bd[0]]={
            'id':info_bd[0],
            'avatar':info_bd[1],
            'avatar_info':info_bd[2],
            'first_name':info_bd[3],
            'nickname':info_bd[4],
            'privilege':info_bd[5],
            'balance_usd':info_bd[6],
            'balance_chy':info_bd[7],
            'btc_usd':info_bd[8],
            'price_buy_btc_usd':info_bd[9],
            'btc_chy':info_bd[10],
            'price_buy_btc_chy':info_bd[11],
            'eth_usd':info_bd[12],
            'price_buy_eth_usd':info_bd[13],
            'eth_chy':info_bd[14],
            'price_buy_eth_chy':info_bd[15],
            'bonus_chy':info_bd[16],
        }
    if p2p.replace('.','',1).isdigit() or p2p.replace(',','',1).isdigit() :
        if float(p2p.replace(',','.'))<=0:
            await message.answer('0 не переводим!?')
            return
        elif json_info[from_p2p]['balance_chy']<float(p2p.replace(',','.')):
            await message.answer('Недостаточно средст!')
            return
        from_user=json_info[from_p2p]['balance_chy']-float(p2p.replace(',','.'))
        for_user=json_info[for_p2p]['balance_chy']+float(p2p.replace(',','.'))
        await cur.execute(f"UPDATE profile SET balance_chy='{round(from_user,3)}' WHERE id='{from_p2p}'")
        await cur.execute(f"UPDATE profile SET balance_chy='{round(for_user,3)}' WHERE id='{for_p2p}'")
        await base.commit()
        await message.answer(f'✅ Перевод {json_info[for_p2p]["nickname"]} уcпешно выполнен!')
        await bot.send_message(chat_id=json_info[for_p2p]["id"],text=f'💸 {json_info[from_p2p]["nickname"]} перевел вам:\n\n➕ 💴: {float(p2p.replace(",","."))} ¥')
        await bot.send_message(chat_id=json_info[from_p2p]["id"],text=f'💸 Вы перевели {json_info[for_p2p]["nickname"]} :\n\n➖ 💴: {float(p2p.replace(",","."))} ¥')
    else:
        await message.answer('Попробуйте еще раз!')
        return 
    await bot.delete_message(chat_id=chat_id,message_id=msg_id)
    await state.finish()


def register_handlers_translate_p2p_chy(dp: Dispatcher):
    dp.register_callback_query_handler(Start_translate_p2p_chy,lambda callback: callback.data.startswith('chy_translate_p2p_'),state=None)
    dp.register_callback_query_handler(cancel_handler_translate_p2p_chy,lambda callback: callback.data.startswith('translate_chy_cancel_'),state="*")
    dp.register_message_handler(translate_p2p_chy, state = FSMtranslate_p2p_chy.p2p)
