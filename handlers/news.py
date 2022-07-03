import json
import datetime
import requests
from aiogram import types, Dispatcher
from aiogram.utils.markdown import hbold,hunderline,hcode,hlink
from website_parse_json import cybersport_parse


async def website_cybersport(message: types.Message):
    # cybersport_parse.check_news_cybersport_update()
    # with open('website_parse_json/news_cybersport.json') as file:
    #     news_list_cybersport=json.load(file)
    # 
    # for k, view in sorted(news_list_cybersport.items(), key=lambda item: item[1]['article_data_timestamp'])[-5:]:
    #     news_cybersport=f"{hbold(datetime.datetime.fromtimestamp(view['article_data_timestamp']))}\n" \
    #                      f"{hlink(view['article_title'],view['article_url'])}"
    #      
    #     await message.answer(news_cybersport)
    response = requests.get(f"https://www.cybersport.ru/api/materials?page%5Boffset%5D=0&page%5Blimit%5D=100&filter%5BtagIds%5D=6974&sort=internalRating")
    news_cybersport_info={}
    for view in response.json()['data']:
        news_cybersport_info[view['id']]={
            'title': view['attributes']['title'],
            'slug': f"https://www.cybersport.ru/tags/games/{view['attributes']['slug']}",
            'time': view['attributes']['publishedAt']
        }
    for k,view in sorted(news_cybersport_info.items(), key=lambda item: item[1]['time'])[-5:]:
        news_cybersport_answer_chat=f"{hbold(datetime.datetime.fromtimestamp(view['time']))}\n" \
                                    f"{hlink(view['title'],view['slug'])}"
        
        await message.answer(news_cybersport_answer_chat)
        
def register_handlers_news(dp: Dispatcher):
    dp.register_message_handler(website_cybersport, commands=['cybersport','киберспорт'])


