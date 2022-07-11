import hashlib
import json,string
from aiogram.utils.markdown import hbold,hunderline,hcode,hlink
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
    if text[:3] != 'gif' and text[:3] != 'гиф' and text[:6] != 'anime_' and text[:6] != 'аниме_':
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
    elif text[:6] != 'anime_' and text[:6] != 'аниме_':
        tenor_api_key='AIzaSyBOcqMmqBT9JD1sLs5y7K-9Q6KRbMcci3g'
        ckey='py teleg bot'
        response=requests.get(f'https://tenor.googleapis.com/v2/search?q={text}&key={tenor_api_key}&client_key={ckey}&limit=100000')
        links=response.json()['results']
        articles=[types.InlineQueryResultGif(
            id=link['id'],
            thumb_url=link['media_formats']['tinygifpreview']['url'],
            gif_url=link['media_formats']['loopedmp4']['url'])for link in links]

        await query.answer(articles,cache_time=60,is_personal=True)
    else:
        text_anime=text[6:]
        if text_anime=='':
            # text_anime='Shadows House'
            response=requests.get(f'https://kodikapi.com/list?token=84079b04f2b985c868f4ef75d5c66b2a&types=anime,anime-serial&with_page_links=true&with_material_data=true/translations')
            links=response.json()['results']
            articles=[types.InlineQueryResultArticle(
                id = link['id'],
                title=f'{link["translation"]["title"]}',
                description=f'{link["title"]}\n{link["title_orig"]}',
                url=link['link'],
                hide_url=True,
                thumb_url=f'{link["screenshots"][0]}',
                input_message_content=types.InputTextMessageContent(
                    message_text=f"{hlink(link['title'],link['link'])}\nозвучка от: {hbold(link['translation']['title'])}")

            ) for link in links]
            await query.answer(articles,cache_time=60,is_personal=True)
        else:
            response=requests.get(f'https://kodikapi.com/search?token=84079b04f2b985c868f4ef75d5c66b2a&types=anime,anime-serial&with_page_links=true&with_material_data=true&title={text_anime}/translations')
            links=response.json()['results']
            articles=[types.InlineQueryResultArticle(
                id = link['id'],
                title=f'{link["translation"]["title"]}',
                description=f'{link["title"]}\n{link["title_orig"]}',
                url=link['link'],
                hide_url=True,
                thumb_url=f'{link["screenshots"][0]}',
                input_message_content=types.InputTextMessageContent(
                    message_text=f"{hlink(link['title'],link['link'])}\nозвучка от: {hbold(link['translation']['title'])}")
        
            ) for link in links]
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


# @dp.inline_handler()
# async def inline_handler(query: types.InlineQuery):
#     text=query.query or 'Shadows House'
#     response=requests.get(f'https://kodikapi.com/search?token=84079b04f2b985c868f4ef75d5c66b2a&types=anime,anime-serial&with_page_links=true&with_material_data=true&title={text}/translations')
#     links=response.json()['results']
#     articles=[types.InlineQueryResultArticle(
#         id = link['id'],
#         title=f'{link["translation"]["title"]}',
#         description=f'{link["title"]}\n{link["title_orig"]}',
#         url=link['link'],
#         hide_url=True,
#         thumb_url=f'{link["screenshots"][0]}',
#         input_message_content=types.InputTextMessageContent(
#         message_text=f"{hlink(link['title'],link['link'])}\nозвучка от: {hbold(link['translation']['title'])}")
# 
#         ) for link in links]
#     await query.answer(articles,cache_time=60,is_personal=True)

        

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