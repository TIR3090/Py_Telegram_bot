import hashlib
import json,string
import requests
from aiogram import types,Dispatcher
from create_bot import dp,bot
from youtube_search import YoutubeSearch

def search_youtube(text):
    res_yt=YoutubeSearch(text,max_results=100).to_dict()
    return res_yt

@dp.inline_handler()
async def inline_handler(query: types.InlineQuery):
    text=query.query or 'echo'
    if text[:3] != 'gif' and text[:3] != 'гиф':
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
    else:
        tenor_api_key='AIzaSyBOcqMmqBT9JD1sLs5y7K-9Q6KRbMcci3g'
        ckey='py teleg bot'
        response=requests.get(f'https://tenor.googleapis.com/v2/search?q={text}&key={tenor_api_key}&client_key={ckey}&limit=100000')
        links=response.json()['results']
        articles=[types.InlineQueryResultGif(
            id=link['id'],
            thumb_url=link['media_formats']['tinygifpreview']['url'],
            gif_url=link['media_formats']['loopedmp4']['url'])for link in links]

        await query.answer(articles,cache_time=60,is_personal=True)
        
        
# @dp.inline_handler()
# async def inline_handler(query: types.InlineQuery):
#     text=query.query or 'echo'
#         tenor_api_key='AIzaSyBOcqMmqBT9JD1sLs5y7K-9Q6KRbMcci3g'
#         ckey='py teleg bot'
#         response=requests.get(f'https://tenor.googleapis.com/v2/search?q={text}&key={tenor_api_key}&client_key={ckey}&limit=100000')
#         links=response.json()['results']
#         
#         # for link in links:
#         #     print(link['media_formats']['tinygifpreview']['url']) 
#         #     print(link['media_formats']['nanogif']['url'])
#         #     print('_____________')
#         articles=[types.InlineQueryResultGif(
#             id=link['id'],
#             thumb_url=link['media_formats']['tinygifpreview']['url'],
#             gif_url=link['media_formats']['loopedmp4']['url'])for link in links]
#         
#         await query.answer(articles,cache_time=60,is_personal=True)
        

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