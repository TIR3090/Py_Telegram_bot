import datetime
import random
from handlers import registration
import psycopg2 as sq
from aiogram import types, Dispatcher
from create_bot import dp,bot
from data_base import sqlite_db
from keyboards import admin_kb,client_kb,news_kb,help_kb



async def bonus(message: types.Message):
    if registration.IsRegistration(message.from_user.id)==False:
        await message.answer('/reg - Вначале зарегистрируйтесь!')
        return
    global base, cur
    base = sq.connect(dbname='d9882ng2h7srs6', user='rixdvqeatezwpn',
                      password='60e4ac9ad7bcb8be1b8900f38fc0c70a52a69fb6dcdd59bf553c6262631f54a6', host='ec2-34-242-8-97.eu-west-1.compute.amazonaws.com')
    cur=base.cursor()
    cur.execute(f"SELECT balance_chy,bonus_chy FROM profile WHERE id='{message.from_user.id}'")
    for inform_v_bd in cur.fetchall():
        if datetime.datetime.now()<inform_v_bd[1]:
            ost_time_bonus=inform_v_bd[1].replace(microsecond=0)-datetime.datetime.now().replace(microsecond=0)
            await message.answer(f'Бонус будет доступен через:\n⌚ {ost_time_bonus}')
        else:
            bonus_nachisl=random.uniform(1000,15001)
            balance_v_bd=int(inform_v_bd[0])+round(bonus_nachisl,3)
            bonus_poluch = datetime.datetime.now() + datetime.timedelta(minutes=90)
            cur.execute(f"UPDATE profile SET balance_chy='{balance_v_bd}',bonus_chy='{bonus_poluch}' WHERE id='{message.from_user.id}'")
            base.commit()
            await message.answer(f"[~~~Бонус получен~~~]\n"
                                 f"💸 {round(bonus_nachisl,3)} ¥\n"
                                 f"⏱ {bonus_poluch.strftime('%H:%M')}\n"
                                 f"[~~~~~~~~~~~~~~~~]")



def register_handlers_bonus_chy(dp: Dispatcher):
    dp.register_message_handler(bonus, commands=['bonus','бонус'])
