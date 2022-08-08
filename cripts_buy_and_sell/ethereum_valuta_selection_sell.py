import psycopg2 as sq
from aiogram import types, Dispatcher
from keyboards import cripts_kb



async def ethereum_valuta_selection_sell(callback: types.CallbackQuery):
    global base, cur
    base = sq.connect(dbname='d9882ng2h7srs6',
                      user='rixdvqeatezwpn',
                      password='60e4ac9ad7bcb8be1b8900f38fc0c70a52a69fb6dcdd59bf553c6262631f54a6',
                      host='ec2-34-242-8-97.eu-west-1.compute.amazonaws.com')
    cur=base.cursor()
    cur.execute(f"SELECT * FROM profile WHERE id='{callback.from_user.id}'")
    for information in cur.fetchall():
        nick=information[4]
        eth_usd=information[12]
        eth_chy=information[14]
    info=f'{nick} крипты на счету:\n' \
         f'Ξ-¥: {"{:0.9f}".format(eth_chy)}\n' \
         f'Ξ-$: {"{:0.9f}".format(eth_usd)}\n\n' \
         f'Выберите кошелек:'
    await callback.message.edit_text(text=info,reply_markup=cripts_kb.ethereum_valuta_selection_sell)
    await callback.answer()



def register_handlers_sell_eth_usd_chy(dp: Dispatcher):
    dp.register_callback_query_handler(ethereum_valuta_selection_sell,text='ethereum_eth_sell')
