import hashlib
import os,json,string
from aiogram import types,Dispatcher
from create_bot import dp,bot
from youtube_search import YoutubeSearch

def search_youtube(text):
    res_yt=YoutubeSearch(text,max_results=100).to_dict()
    return res_yt

@dp.inline_handler()
async def inline_handler(query: types.InlineQuery):
    text=query.query or 'echo'
    links=search_youtube(text)
    articles=[types.InlineQueryResultArticle(
        id = hashlib.md5(f'{link["id"]}'.encode()).hexdigest(),
        title=f'{link["title"]}',
        url=f'https://www.youtube.com/watch?v={link["id"]}',
        thumb_url=f'{link["thumbnails"][0]}',
        input_message_content=types.InputTextMessageContent(
            message_text=f'https://www.youtube.com/watch?v={link["id"]}')
        
    ) for link in links]

    await query.answer(articles,cache_time=60,is_personal=True)
# @dp.message_handler()
async def echo_send(message: types.Message):
    if{i.lower().translate(str.maketrans('','',string.punctuation)) for i in message.text.split(' ')} \
            .intersection(set(json.load(open('clear/clear.json'))))!=set():
        await message.reply('Ильдар лох!')
        await message.delete()
    print(f'{message.from_user.first_name} написал: {message.text}\n')
    # print(message.text)
    # if message.text =='Привет':
    # # await message.answer(message.text)
    #     await message.reply('Хай!')

def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)
    # dp.register_message_handler()
    # dp.register_message_handler()