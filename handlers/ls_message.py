import asyncio
# import psycopg2 as sq
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher.filters import Text
from handlers import registration
from create_bot import dp,bot
import aiosqlite as aoisq




class FSMmessage_ls(StatesGroup):
    message_v_ls=State()
    message_id=State()

async  def cancel_handler_mess(message: types.Message,state:FSMContext):
    current_state=await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('отмена!')

async  def start_ls_message(message: types.Message,state:FSMContext):
    if await registration.IsRegistration(message.from_user.id)==False:
        await message.answer('/reg - Вначале зарегистрируйтесь!')
        return
    await message.reply('/cancel- отмена\n\n'
                        'Введите текст:')
    await FSMmessage_ls.message_v_ls.set()
    await asyncio.sleep(180)
    current_state=await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Время ожидания вышло!')



async  def ls_message_text(message: types.Message,state:FSMContext):
    async with  state.proxy() as data:
        data['message_v_ls']=message.text
        await FSMmessage_ls.message_id.set()
    await message.reply('/cancel- отмена\n\n'
                        'Введите id получателя:')


async def ls_message_id_polzovatel(message: types.Message,state: FSMContext):
    global base, cur
    # base = sq.connect(dbname='d9882ng2h7srs6', user='rixdvqeatezwpn',
    #                   password='60e4ac9ad7bcb8be1b8900f38fc0c70a52a69fb6dcdd59bf553c6262631f54a6', host='ec2-34-242-8-97.eu-west-1.compute.amazonaws.com')
    # cur=base.cursor()
    base =await aoisq.connect("data_base/data_casino_keeper.db")
    cur=await base.cursor()
    id_poluchatelya=message.text
    text_answer_v_ls=await state.get_data()
    answer_v_ls=text_answer_v_ls.get('message_v_ls')
    if id_poluchatelya.isdigit():
        await cur.execute(f"SELECT * FROM profile WHERE id ='{id_poluchatelya}'")
        polzovatel_id=await cur.fetchone()
        if polzovatel_id is None:
            await message.answer('❌ Пользователь не найден!\n')
            await message.answer('Попробуйте еще раз!')
            return
        else:
            await bot.send_message(polzovatel_id[0],f'От {message.from_user.first_name}:\n{answer_v_ls}')
            await message.answer(f"✅ {polzovatel_id[3]}, дотаставлено!")
    elif id_poluchatelya.lower()=='all' or id_poluchatelya.lower()=='все' or id_poluchatelya.lower()=='всем':
        await cur.execute(f"SELECT * FROM profile")
        for information in await cur.fetchall():
            if information[0]!= f'{message.from_user.id}':
                await bot.send_message(information[0],f'От {message.from_user.first_name}:\n{answer_v_ls}')
                await message.answer(f"✅ {information[3]}, дотаставлено!")
    else:
        await message.answer(f"Введи id или all(всем)!")
        return 
    await message.answer(f"Рассылка закончилась!")
    await state.finish()

def register_handlers_ls_message(dp: Dispatcher):
    dp.register_message_handler(start_ls_message, commands=['mess','месс'], state=None)
    dp.register_message_handler(cancel_handler_mess, state="*", commands =['отмена','cancel'])
    dp.register_message_handler(cancel_handler_mess,Text(equals=['отмена','cancel'], ignore_case=True),state="*")
    dp.register_message_handler(ls_message_text,state = FSMmessage_ls.message_v_ls)
    dp.register_message_handler(ls_message_id_polzovatel, state = FSMmessage_ls.message_id)
