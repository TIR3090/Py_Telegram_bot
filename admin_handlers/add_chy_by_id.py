import asyncio
# import psycopg2 as sq
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher.filters import Text
from handlers import registration
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton, InlineKeyboardMarkup,InlineKeyboardButton
from config import DEVELOPER
from create_bot import dp, bot
import aiosqlite as aoisq




class FSM_add_chy(StatesGroup):
    recipients_id=State()
    add_chy_to_the_balance=State()
    delet_msg=State()
    chat_id=State()
    
    
    
async  def cancel_handler_add_chy_to_the_balance(callback: types.CallbackQuery,state:FSMContext):
    add_chy_cancel=callback.data.split('_')[3]
    if callback.from_user.id == int(add_chy_cancel):
        await callback.message.delete()
        current_state=await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await callback.message.answer('Отмена!')
    else:
        await callback.answer(text='Не твое сообщени!', show_alert=True)

async  def start_add_chy(message: types.Message,state:FSMContext):
    if message.from_user.id == DEVELOPER:
        add_chy_cancel=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Отмена',callback_data=f'addchy_recipients_cancel_{message.from_user.id}'))
        msg = await message.answer('id:',reply_markup=add_chy_cancel)
        async with state.proxy() as data:
            data['delet_msg']=msg.message_id
            data['chat_id']=msg.chat.id
        await FSM_add_chy.recipients_id.set()
        await asyncio.sleep(180)
        current_state=await state.get_state()
        if current_state is None:
            return
        await bot.delete_message(chat_id=msg.chat.id,message_id=msg.message_id)
        await state.finish()
        await message.reply('Время ожидания вышло!')



async  def search_id_text(message: types.Message,state:FSMContext):
    global base, cur
    base =await aoisq.connect("data_base/data_casino_keeper.db")
    cur=await base.cursor()
    id_poluchatelya_chy=message.text
    if id_poluchatelya_chy.isdigit():
        await cur.execute(f"SELECT * FROM profile WHERE id ='{id_poluchatelya_chy}'")
        chy_polzovatel_id=await cur.fetchone()
        if chy_polzovatel_id is None:
            await message.answer('❌ Пользователь не найден!\n')
            return
        else:
            async with state.proxy() as data:
                    data['recipients_id']=id_poluchatelya_chy
            await message.answer(f"Сумма начисления:")
            await FSM_add_chy.add_chy_to_the_balance.set()
    else:
        await message.answer(f"Введи id!")
        return



async def add_chy_polzovatel(message: types.Message,state: FSMContext):
    chy_p2p=message.text
    if chy_p2p.isdigit():
        async with state.proxy() as data:
            data['add_chy_to_the_balance']=chy_p2p
        chy_get=await state.get_data()
        chy_p2p_dig=chy_get.get('add_chy_to_the_balance')
        msg_id=chy_get.get('delet_msg')
        chat_id=chy_get.get('chat_id')
        id_p2p=chy_get.get('recipients_id')
        await cur.execute(f"SELECT * FROM profile WHERE id ='{id_p2p}'")
        chy_polzovatel_id=await cur.fetchone()
        balance_chy_by_polz=chy_polzovatel_id[7]+round(float(chy_p2p_dig),3)
        await cur.execute(f"UPDATE profile SET balance_chy='{round(balance_chy_by_polz,3)}' WHERE id='{id_p2p}'")
        await base.commit()
        await bot.send_message(chy_polzovatel_id[0],f'От <b>DEVELOPER</b>:\n➕ 💴: {round(float(chy_p2p_dig),3)} ¥')
        await message.answer(f"✅ {chy_polzovatel_id[3]}, начислено!")
        await bot.delete_message(chat_id=chat_id,message_id=msg_id)
        await state.finish()
    elif chy_p2p<=0:
        await message.answer(f"Введи сумму!")
    else:
        await message.answer(f"Введи сумму!")
        return

def register_handlers_add_chy_developer(dp: Dispatcher):
    dp.register_message_handler(start_add_chy, commands=['add_chy_deleloper'], state=None)
    dp.register_callback_query_handler(cancel_handler_add_chy_to_the_balance,lambda callback: callback.data.startswith('addchy_recipients_cancel_'),state="*")
    dp.register_message_handler(search_id_text,state = FSM_add_chy.recipients_id)
    dp.register_message_handler(add_chy_polzovatel, state = FSM_add_chy.add_chy_to_the_balance)
