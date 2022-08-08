from aiogram import types, Dispatcher
import gtts
from create_bot import bot
from bs4 import BeautifulSoup
import asyncio
from create_bot import dp, bot
import psycopg2 as sq
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher.filters import Text
from handlers import registration
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton, InlineKeyboardMarkup,InlineKeyboardButton



class FSMvoice(StatesGroup):
    voice=State()
    delet_msg=State()
    chat_id=State()



async  def cancel_handler_voice(callback: types.CallbackQuery,state:FSMContext):
    voice_cancel=callback.data.split('_')[1]
    if callback.from_user.id == int(voice_cancel):
        await callback.message.delete()
        current_state=await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await callback.message.answer('Отмена!')
    else:
        await callback.answer(text='Не твое сообщени!', show_alert=True)


async def Start_voice(message: types.Message,state: FSMContext):
    voice_cancel=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Отмена',callback_data=f'voice_{message.from_user.id}'))
    msg = await message.answer('Введите текст:',reply_markup=voice_cancel)
    async with state.proxy() as data:
        data['delet_msg']=msg.message_id
        data['chat_id']=msg.chat.id
    await FSMvoice.voice.set()
    await asyncio.sleep(60)
    current_state=await state.get_state()
    if current_state is None:
        return
    await bot.delete_message(chat_id=msg.chat.id,message_id=msg.message_id)
    await state.finish()
    await message.answer('Время ожидания вышло!')



async def Voice_message(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['voice']=message.text
    voice_get=await state.get_data()
    voice=voice_get.get('voice')
    msg_id=voice_get.get('delet_msg')
    chat_id=voice_get.get('chat_id')
    me=await bot.get_me()
    # voice_text=message.text[7:]
    voice_bot=gtts.gTTS(f'{voice}',lang="ru")
    voice_bot.save('voice.mp3')
    await message.answer_audio(open('voice.mp3','rb'),performer=f"{me.first_name}",title=f'{message.from_user.first_name} текст озвучен:')
    await bot.delete_message(chat_id=chat_id,message_id=msg_id)
    await state.finish()
    
    
    
# async def voice_message_handler(message: types.Message):
#     await message.voice.download(destination_file=f"voice_to_text.mp3")
#     recog =v_t.Recognizer()
#     with v_t.AudioFile("voice_message/voice_to_text.wav") as audio_file:
#         audio=recog.record(audio_file)
#     query= recog.recognize_google(audio)
#     await message.answer(query.lower())
    
def register_handlers_voice(dp: Dispatcher):
    dp.register_message_handler(Start_voice, commands=['voice','голос'],state=None)
    # dp.register_message_handler(voice_message_handler,content_types=[ContentType.VOICE])
    dp.register_callback_query_handler(cancel_handler_voice,lambda callback: callback.data.startswith('voice_'),state="*")
    dp.register_message_handler(Voice_message, state = FSMvoice.voice)
