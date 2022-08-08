import random
import requests
from aiogram import types, Dispatcher
from translate import Translator
from bs4 import BeautifulSoup
import asyncio
from create_bot import dp, bot
import psycopg2 as sq
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher.filters import Text
from handlers import registration
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton, InlineKeyboardMarkup,InlineKeyboardButton



class FSMgif_tenor(StatesGroup):
    gif_tenor=State()
    delet_msg=State()
    chat_id=State()



async  def cancel_handler_gif_tenor(callback: types.CallbackQuery,state:FSMContext):
    gif_tenor_cancel=callback.data.split('_')[2]
    if callback.from_user.id == int(gif_tenor_cancel):
        await callback.message.delete()
        current_state=await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await callback.message.answer('Отмена поиска гифки в тенор!')
    else:
        await callback.answer(text='Не твое сообщени!', show_alert=True)


async def Start_search_gif_tenor(message: types.Message,state: FSMContext):
    gif_tenor_cancel=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Отмена',callback_data=f'gif_tenor_{message.from_user.id}'))
    msg = await message.answer('Искать гифку в Tenor:',reply_markup=gif_tenor_cancel)
    async with state.proxy() as data:
        data['delet_msg']=msg.message_id
        data['chat_id']=msg.chat.id
    await FSMgif_tenor.gif_tenor.set()
    await asyncio.sleep(60)
    current_state=await state.get_state()
    if current_state is None:
        return
    await bot.delete_message(chat_id=msg.chat.id,message_id=msg.message_id)
    await state.finish()
    await message.answer('Время ожидания вышло!')



async def GIF_tenor(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['gif_tenor']=message.text
    gif_tenor_get=await state.get_data()
    gif_tenor=gif_tenor_get.get('gif_tenor')
    msg_id=gif_tenor_get.get('delet_msg')
    chat_id=gif_tenor_get.get('chat_id')
    # trans=Translator(from_lang='ru',to_lang='en')
    # gifki_zapr=message.text[5:]
    # en_form=trans.translate(gifki_zapr)
    tenor_api_key='AIzaSyBOcqMmqBT9JD1sLs5y7K-9Q6KRbMcci3g'
    ckey='py teleg bot'
    # response = requests.get(f"https://tenor.com/search/{gifki_zapr}-gifs")
    # soup=BeautifulSoup(response.text,features="html.parser")
    gifs = []
    # soup.findAll()
    # for gif in soup.findAll('img'):
    #     gifs.append(gif.get('src'))
    response = requests.get(f"https://tenor.googleapis.com/v2/search?q={gif_tenor}&key={tenor_api_key}&client_key={ckey}&limit=100000")
    for view in response.json()['results']:
        gifs.append(view['url'])
    await message.answer_animation(random.choice(gifs))
    await bot.delete_message(chat_id=chat_id,message_id=msg_id)
    await state.finish()



def register_handlers_gif_random(dp: Dispatcher):
    dp.register_message_handler(Start_search_gif_tenor, commands=['gif','гиф'],state=None)
    dp.register_callback_query_handler(cancel_handler_gif_tenor,lambda callback: callback.data.startswith('gif_tenor_'),state="*")
    dp.register_message_handler(GIF_tenor, state = FSMgif_tenor.gif_tenor)
