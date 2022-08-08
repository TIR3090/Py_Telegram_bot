from handlers import registration
import wikipedia
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



class FSMwiki(StatesGroup):
    wiki=State()
    delet_msg=State()
    chat_id=State()



async  def cancel_handler_wiki(callback: types.CallbackQuery,state:FSMContext):
    wiki_cancel=callback.data.split('_')[1]
    if callback.from_user.id == int(wiki_cancel):
        await callback.message.delete()
        current_state=await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await callback.message.answer('Отмена поиска в wiki!')
    else:
        await callback.answer(text='Не твое сообщени!', show_alert=True)


async def Start_search_wiki(message: types.Message,state: FSMContext):
    wiki_cancel=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Отмена',callback_data=f'wiki_{message.from_user.id}'))
    msg = await message.answer('Искать в wiki:',reply_markup=wiki_cancel)
    async with state.proxy() as data:
        data['delet_msg']=msg.message_id
        data['chat_id']=msg.chat.id
    await FSMwiki.wiki.set()
    await asyncio.sleep(60)
    current_state=await state.get_state()
    if current_state is None:
        return
    await bot.delete_message(chat_id=msg.chat.id,message_id=msg.message_id)
    await state.finish()
    await message.answer('Время ожидания вышло!')


async  def inform_wiki_pedia(message: types.Message,state: FSMContext):
    try:
        async with state.proxy() as data:
            data['wiki']=message.text
        wiki_get=await state.get_data()
        wiki=wiki_get.get('wiki')
        msg_id=wiki_get.get('delet_msg')
        chat_id=wiki_get.get('chat_id')
        wikipedia.set_lang("ru")
        # wiki_post=message.text[6:]
        push_wiki=wikipedia.summary(f"{wiki}")
        # push_wiki_all_info= wikipedia.page(f"{wiki_post}").content
        # push_wiki_all_info1= wikipedia.search(f"{wiki_post}")
        # await message.reply(push_wiki_all_info1)
        # print(push_wiki_all_info)
        await message.answer(push_wiki)
        await bot.delete_message(chat_id=chat_id,message_id=msg_id)
        await state.finish()
    except:
        push_wiki_search= wikipedia.search(f"{wiki}")
        await message.answer(push_wiki_search)
        await bot.delete_message(chat_id=chat_id,message_id=msg_id)
        await state.finish()



def register_handlers_search_wiki(dp: Dispatcher):
    dp.register_message_handler(Start_search_wiki, commands=['wiki','вики'],state=None)
    dp.register_callback_query_handler(cancel_handler_wiki,lambda callback: callback.data.startswith('wiki_'),state="*")
    dp.register_message_handler(inform_wiki_pedia, state = FSMwiki.wiki)
