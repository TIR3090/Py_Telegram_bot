import json
import datetime
import requests
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold,hunderline,hcode,hlink
from bs4 import BeautifulSoup
from website_parse_json import cybersport_parse
from keyboards import client_kb,news_kb



async def website_ixbt(message: types.Message):
    await message.answer(f'<b>ixbt</b>\nВыберите кол-во новостей:',reply_markup=news_kb.news_ixbt_games_kolv)



async def five_news_ixbt_games(callback: types.CallbackQuery):
    await callback.message.delete()
    response = requests.get(f"https://ixbt.games/news/")
    soup=BeautifulSoup(response.text,features="lxml")
    news_ixbt_info={}
    for article in soup.find_all("div",class_="py-2"):
        article_url = article.find("a",class_="card-link").get("href")
        article_url_link_id = article_url.split('/')[-1]
        article_time=article.find("div",class_="badge badge-time").text.strip()
        article_title = article.find("a",class_="card-link").text.strip()
        # article_soder=article.find("div",class_="d-flex d-sm-block my-2").text.strip()
        # print(article_soder)
        news_ixbt_info[article_url_link_id]={
            'title': article_title,
            'url': f"https://ixbt.games{article_url}",
            'time': article_time
        }
    for k,view in sorted(news_ixbt_info.items(), key=lambda item: item[1]['time'])[-5:]:
        news_ixbt_answer_chat=f"{hbold(view['time'])}\n" \
                              f"{hlink(view['title'],view['url'])}"
        await callback.message.answer(news_ixbt_answer_chat)
    await callback.answer()

async def all_news_ixbt_games(callback: types.CallbackQuery):
    await callback.message.delete()
    response = requests.get(f"https://ixbt.games/news/")
    soup=BeautifulSoup(response.text,features="lxml")
    news_ixbt_info={}
    for article in soup.find_all("div",class_="py-2"):
        article_url = article.find("a",class_="card-link").get("href")
        article_url_link_id = article_url.split('/')[-1]
        article_time=article.find("div",class_="badge badge-time").text.strip()
        article_title = article.find("a",class_="card-link").text.strip()
        # article_soder=article.find("div",class_="d-flex d-sm-block my-2").text.strip()
        # print(article_soder)
        news_ixbt_info[article_url_link_id]={
            'title': article_title,
            'url': f"https://ixbt.games{article_url}",
            'time': article_time
        }
    for k,view in sorted(news_ixbt_info.items(), key=lambda item: item[1]['time'])[-20:]:
        news_ixbt_answer_chat=f"{hbold(view['time'])}\n" \
                              f"{hlink(view['title'],view['url'])}"
        await callback.message.answer(news_ixbt_answer_chat)
    await callback.answer()


async def ten_news_ixbt_games(callback: types.CallbackQuery):
    await callback.message.delete()
    response = requests.get(f"https://ixbt.games/news/")
    soup=BeautifulSoup(response.text,features="lxml")
    news_ixbt_info={}
    for article in soup.find_all("div",class_="py-2"):
        article_url = article.find("a",class_="card-link").get("href")
        article_url_link_id = article_url.split('/')[-1]
        article_time=article.find("div",class_="badge badge-time").text.strip()
        article_title = article.find("a",class_="card-link").text.strip()
        # article_soder=article.find("div",class_="d-flex d-sm-block my-2").text.strip()
        # print(article_soder)
        news_ixbt_info[article_url_link_id]={
            'title': article_title,
            'url': f"https://ixbt.games{article_url}",
            'time': article_time
        }
    for k,view in sorted(news_ixbt_info.items(), key=lambda item: item[1]['time'])[-10:]:
        news_ixbt_answer_chat=f"{hbold(view['time'])}\n" \
                              f"{hlink(view['title'],view['url'])}"
        await callback.message.answer(news_ixbt_answer_chat)
    await callback.answer()



async def website_news_ixbt_games(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(f'<b>ixbt</b>\nВыберите кол-во новостей:',reply_markup=news_kb.news_ixbt_games_kolv)
    await callback.answer()



def register_handlers_news(dp: Dispatcher):
    dp.register_message_handler(website_ixbt, commands=['ixbt','иксбт'])
    # dp.register_message_handler(website_cybersport,Text(equals=['📰 news','📰 новости']))
    dp.register_callback_query_handler(five_news_ixbt_games,text='5_newns_ixbt_games')
    dp.register_callback_query_handler(all_news_ixbt_games,text='all_newns_ixbt_games')
    dp.register_callback_query_handler(ten_news_ixbt_games,text='10_newns_ixbt_games')
    dp.register_callback_query_handler(website_news_ixbt_games,text='ixbt_news')
