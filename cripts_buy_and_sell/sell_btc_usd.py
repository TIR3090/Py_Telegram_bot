import asyncio
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



class FSMsellbitcoin_usd(StatesGroup):
    kol_btc=State()
    delet_msg=State()
    chat_id=State()


async def start_sell_usd(callback: types.CallbackQuery,state: FSMContext):
    await callback.message.delete()
    if await registration.IsRegistration(callback.from_user.id)==False:
        await callback.message.answer('/reg - Вначале зарегистрируйтесь!')
        return
    cancel_handler_cripts_sell=InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton(text='Отмена',callback_data=f'cancel_state_cripts_sell_{callback.from_user.id}'))
    msg = await callback.message.answer('Введите количество BTC ($):',reply_markup=cancel_handler_cripts_sell)
    async with state.proxy() as data:
        data['delet_msg']=msg.message_id
        data['chat_id']=msg.chat.id
    await FSMsellbitcoin_usd.kol_btc.set()
    await asyncio.sleep(120)
    current_state=await state.get_state()
    if current_state is None:
        return
    await bot.delete_message(chat_id=msg.chat.id,message_id=msg.message_id)
    await state.finish()
    await callback.message.answer('Время ожидания вышло!')



async def sell_btc_usd(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['kol_btc']=message.text
    kol_sell=await state.get_data()
    kol_sell_btc=kol_sell.get('kol_btc')
    msg_id=kol_sell.get('delet_msg')
    chat_id=kol_sell.get('chat_id')
    if kol_sell_btc.replace('.','',1).isdigit() or kol_sell_btc.replace(',','',1).isdigit() :
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
            balance_btc_usd=data_bd[8]
            balance_usd=data_bd[6]
            nickname=data_bd[4]
        if float(kol_sell_btc.replace(',','.'))<=0:
            await message.answer('0 BTC ($) !?')
            return
        elif balance_btc_usd<float(kol_sell_btc.replace(',','.')):
            await message.answer('❌ Недостаточно BTC ($) !')
            return
        kol_btc_usd_pol=float(kol_sell_btc)*json_valute['14']['usd']
        kol_btc_sell=balance_usd+kol_btc_usd_pol
        balance_btc_usd_v_bd_write=balance_btc_usd-float(kol_sell_btc)
        await cur.execute(f"UPDATE profile SET balance_usd={round(kol_btc_sell,3)},btc_usd={round(balance_btc_usd_v_bd_write,9)} WHERE id='{message.from_user.id}'")
        await base.commit()
        await message.delete()
        await message.answer(f"✅ {nickname} продал:\nBTC в $: {'{:0.9f}'.format(float(kol_sell_btc))}\nПолучил: {round(kol_btc_usd_pol,3)} $")
        await bot.delete_message(chat_id=chat_id,message_id=msg_id)
        await state.finish()
    else:
        await message.answer('Некорректная количество!')
        return



def register_handlers_sell_btc_usd(dp: Dispatcher):
    dp.register_callback_query_handler(start_sell_usd,text='bitcoin_valuta_usd_sell',state=None)
    dp.register_message_handler(sell_btc_usd,state=FSMsellbitcoin_usd.kol_btc)
