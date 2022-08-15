import asyncio
import datetime
# import psycopg2 as sq
from aiogram import types, Dispatcher
from create_bot import dp,bot
from data_base import sqlite_db
from keyboards import admin_kb,client_kb,news_kb,help_kb
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher.filters import Text
import base64
import aiosqlite as aoisq



class FSMregistration(StatesGroup):
    id=State()
    photo=State()
    photo_info=State()
    first_name=State()
    nickname=State()
    bonus_chy=State()


async  def cancel_handler(message: types.Message,state:FSMContext):
    current_state=await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('❌ Регистрация отменена!')


async def Start_registration(message: types.Message,state:FSMContext):
    if await IsRegistration(message.from_user.id)==True:
        await message.answer('Вы уже зарегистрированы!')
        return
    await FSMregistration.photo.set()
    await message.reply('/cancel- отмена\nЗагрузи фото для профиля:')
    await asyncio.sleep(90)
    current_state=await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Время ожидания вышло!')

async def reg_Photo_profile_load_photo(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['id']=message.from_user.id
        await message.photo[-1].download(destination_file=f"profiles_photos/encoding.jpg")
        with open(f"profiles_photos/encoding.jpg", "rb") as image_file:
            tmp = base64.b64encode(image_file.read()).decode()
        data['photo']= str(tmp)
        data['photo_info']=message.photo[0].file_id 
    await FSMregistration.nickname.set()
    await message.reply('/cancel- отмена\nВведите ник:')

async def reg_Nickname_profile(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['first_name']=message.from_user.first_name
        data['nickname']=message.text
        data['bonus_chy']=datetime.datetime.now()
    await message.answer("✅ Регистрация прошла успешно!",reply_markup=client_kb.kb_menu)

    await sqlite_db.write_regist_prof(state)

    await state.finish()



async def IsRegistration(fromId):
    global base, cur
    # base = sq.connect(dbname='d9882ng2h7srs6',
    #                   user='rixdvqeatezwpn',
    #                   password='60e4ac9ad7bcb8be1b8900f38fc0c70a52a69fb6dcdd59bf553c6262631f54a6',
    #                   host='ec2-34-242-8-97.eu-west-1.compute.amazonaws.com')
    # cur=base.cursor()
    base =await aoisq.connect("data_base/data_casino_keeper.db")
    cur=await base.cursor()
    await cur.execute(f"SELECT COUNT(*) FROM profile WHERE id='{fromId}'")
    result=await cur.fetchall()
    if result[0] == (1,):
        return True
    return False



def register_handlers_registration(dp: Dispatcher):
    dp.register_message_handler(Start_registration, commands=['start','старт','reg','рег'],start=None)
    dp.register_message_handler(cancel_handler, state="*", commands =['отмена','cancel'])
    dp.register_message_handler(cancel_handler,Text(equals=['отмена','cancel'], ignore_case=True),state="*")
    dp.register_message_handler(reg_Photo_profile_load_photo, content_types=['photo'], state = FSMregistration.photo)
    dp.register_message_handler(reg_Nickname_profile, state = FSMregistration.nickname)
