# import psycopg2 as sq
from aiogram import types, Dispatcher
from keyboards import cripts_kb
import aiosqlite as aoisq



async def ethereum_valuta_selection_buy(callback: types.CallbackQuery):
    global base, cur
    # base = sq.connect(dbname='d9882ng2h7srs6',
    #                   user='rixdvqeatezwpn',
    #                   password='60e4ac9ad7bcb8be1b8900f38fc0c70a52a69fb6dcdd59bf553c6262631f54a6',
    #                   host='ec2-34-242-8-97.eu-west-1.compute.amazonaws.com')
    # cur=base.cursor()
    base =await aoisq.connect("data_base/data_casino_keeper.db")
    cur=await base.cursor()
    await cur.execute(f"SELECT * FROM profile WHERE id='{callback.from_user.id}'")
    for information in await cur.fetchall():
        nick=information[4]
        balance_usd=information[6]
        balance_chy=information[7]
    info=f'{nick} на счету:\n' \
         f'💴 ¥: {balance_chy}\n' \
         f'💵 $: {balance_usd}\n\n' \
         f'Выберите валюту:'
    await callback.message.edit_text(text=info,reply_markup=cripts_kb.ethereum_valuta_selection_buy)
    await callback.answer()



def register_handlers_buy_eth_usd_chy(dp: Dispatcher):
    dp.register_callback_query_handler(ethereum_valuta_selection_buy,text='ethereum_eth_buy')
