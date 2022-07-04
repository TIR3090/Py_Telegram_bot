import json
import time
import datetime
import random
import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp

def ixbt_parse():
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
        news_ixbt_answer_chat=f"{view['time']}\n" \
                                    f"{view['title'],view['url']}"
        print(news_ixbt_answer_chat)

# ixbt_parse()