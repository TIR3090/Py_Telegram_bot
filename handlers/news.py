import json
import datetime
from create_bot import dp, bot
from aiogram import types, Dispatcher
from aiogram.utils.markdown import hbold,hunderline,hcode,hlink
from website_parse_json import cybersport_parse


async def website_cybersport(message: types.Message):
    cybersport_parse.check_news_cybersport_update()
    with open('website_parse_json/news_cybersport.json') as file:
        news_list_cybersport=json.load(file)
    
    for k, view in sorted(news_list_cybersport.items(), key=lambda item: item[1]['article_data_timestamp'])[-5:]:
        news_cybersport=f"{hbold(datetime.datetime.fromtimestamp(view['article_data_timestamp']))}\n" \
                         f"{hlink(view['article_title'],view['article_url'])}"
         
        await message.answer(news_cybersport)



def register_handlers_news(dp: Dispatcher):
    dp.register_message_handler(website_cybersport, commands=['cybersport','киберспорт'])


