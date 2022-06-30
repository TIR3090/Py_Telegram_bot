import os,json,string
from aiogram import types,Dispatcher
from create_bot import dp,bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import admin_kb


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()

#Выход из состояний
async  def cancel_handler(message: types.Message,state:FSMContext):
    current_state=await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Ок')


#Начало диалога
async def cm_start(message: types.Message):
    await FSMAdmin.photo.set()
    await message.reply('Загрузи фото')
    
#ловим 1 ответ
async def load_photo(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['photo']=message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('1 - Текст')

#ловим 2 ответ
async def load_name(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['name']=message.text
        await FSMAdmin.next()
        await message.reply('2 - Teкст')

#ловим 3 ответ
async def load_description(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['description']=message.text
        await FSMAdmin.next()
        await message.reply('3 - Teкст')

#последний ответ
async def load_price(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['price']=float(message.text)
        
    # async with state.proxy() as data:
    #     await message.reply(str(data))
    
    await sqlite_db.sql_add_command(state)
  
    await state.finish()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['загрузить'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands =['отмена','cancel'])
    dp.register_message_handler(cancel_handler,Text(equals=['отмена','cancel'], ignore_case=True),state="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state = FSMAdmin.photo)
    dp.register_message_handler(load_name, state = FSMAdmin.name)
    dp.register_message_handler(load_description, state =FSMAdmin.description)
    dp.register_message_handler(load_price, state = FSMAdmin.price)
