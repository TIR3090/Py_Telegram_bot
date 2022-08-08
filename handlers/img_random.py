import random
import requests
from aiogram import types, Dispatcher
from bs4 import BeautifulSoup
import asyncio
from create_bot import dp, bot
import psycopg2 as sq
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher.filters import Text
from handlers import registration
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton, InlineKeyboardMarkup,InlineKeyboardButton



class FSMimg(StatesGroup):
    image=State()
    delet_msg=State()
    chat_id=State()



async  def cancel_handler_img(callback: types.CallbackQuery,state:FSMContext):
    img_cancel=callback.data.split('_')[1]
    if callback.from_user.id == int(img_cancel):
        await callback.message.delete()
        current_state=await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await callback.message.answer('Отмена поиска картинки!')
    else:
        await callback.answer(text='Не твое сообщени!', show_alert=True)


async def Start_search_img(message: types.Message,state: FSMContext):
    img_cancel=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Отмена',callback_data=f'img_{message.from_user.id}'))
    msg = await message.answer('Искать:',reply_markup=img_cancel)
    async with state.proxy() as data:
        data['delet_msg']=msg.message_id
        data['chat_id']=msg.chat.id
    await FSMimg.image.set()
    await asyncio.sleep(60)
    current_state=await state.get_state()
    if current_state is None:
        return
    await bot.delete_message(chat_id=msg.chat.id,message_id=msg.message_id)
    await state.finish()
    await message.answer('Время ожидания вышло!')



async def image_yandex(message: types.Message,state: FSMContext):
    async with  state.proxy() as data:
        data['image']=message.text
    image_get=await state.get_data()
    image=image_get.get('image')
    msg_id=image_get.get('delet_msg')
    chat_id=image_get.get('chat_id')
    response = requests.get(f"https://yandex.ru/images/search?text={image}&from=tabbar")
    soup = BeautifulSoup(response.text, features="html.parser")
    images = []
    for img in soup.findAll('img'):
        images.append(img.get('src'))
    await message.answer_photo("https:"+random.choice(images))
    await bot.delete_message(chat_id=chat_id,message_id=msg_id)
    await state.finish()



def register_handlers_img_random(dp: Dispatcher):
    dp.register_message_handler(Start_search_img, commands=['img','имг'],state=None)
    dp.register_callback_query_handler(cancel_handler_img,lambda callback: callback.data.startswith('img_'),state="*")
    dp.register_message_handler(image_yandex, state = FSMimg.image)
