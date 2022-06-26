from aiogram import types, Dispatcher
import gtts
import speech_recognition as v_t
from aiogram.types import ContentType


async def Voice_message(message: types.Message):
    try:
        voice_text=message.text[7:]
        voice_bot=gtts.gTTS(f'{voice_text}',lang="ru")
        voice_bot.save('voice.mp3')
        await message.answer_audio(open('voice.mp3','rb'),performer=f"{voice_text}",title=f'{message.from_user.first_name} текст озвучен:')
    except:
        await  message.reply('/voice <Текст для озвучки>\n/голос <Текст для озвучки>')

# async def voice_message_handler(message: types.Message):
#     await message.voice.download(destination_file=f"voice_to_text.mp3")
#     recog =v_t.Recognizer()
#     with v_t.AudioFile("voice_message/voice_to_text.wav") as audio_file:
#         audio=recog.record(audio_file)
#     query= recog.recognize_google(audio)
#     await message.answer(query.lower())
    
def register_handlers_voice(dp: Dispatcher):
    dp.register_message_handler(Voice_message, commands=['voice','голос'])
    # dp.register_message_handler(voice_message_handler,content_types=[ContentType.VOICE])
