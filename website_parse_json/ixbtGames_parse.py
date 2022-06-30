import json
import time
from datetime import datetime
import random

import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp

# def ixbtGames_parse():
#     response = requests.get(f"https://www.cybersport.ru/api/materials?page%5Boffset%5D=25&page%5Blimit%5D=25&filter%5BtagIds%5D=6974&sort=internalRating")
#     soup=BeautifulSoup(response.text,features="lxml")
#     link_CocWY=soup.find_all("p")
# 
#     print(link_CocWY)
#     # news_dict_cybersport = {}
#     # for article in link_CocWY:
#     #     article_title = article.find('h3', class_="title_nSS03").text.strip()
#     #     article_url=f'https://www.cybersport.ru{article.get("href")}'
#     # 
#     #     article_data_time = article.find("time").get("datetime")
#     #     date_from_iso = datetime.fromisoformat(article_data_time)
#     #     date_time=datetime.strftime(date_from_iso,"%Y-%m-%d %H:%M:%S")
#     #     article_data_timestamp=time.mktime(datetime.strptime(date_time,"%Y-%m-%d %H:%M:%S").timetuple())
#     # 
#     #     article_id = article_url.split('/')[-1]
#     #     # article_id =article_id[:4]
#     # 
#     #     # print(f'{article_title} | {article_url} | {article_data_timestamp}')
#     #     # print(f'{article_data_timestamp}')
#     #     news_dict_cybersport[article_id] = {
#     #         "article_data_timestamp" : article_data_timestamp,
#     #         "article_title" : article_title,
#     #         "article_url" : article_url
#     #     }
#     with open('news_ixbtGames.json','w') as file:
#         json.dump(response.json(),file,indent=3, ensure_ascii=False)
# 
# # def test():
# #     with open('news_ixbtGames.json') as file:
# #         news_list_cybersport=json.load(file)
# # 
# #     for view in news_list_cybersport['data']:
# #         # news_cybersport=f"{(view['data'][1]['id'])}\n"
# #         print(view['attributes']['slug'])
# # # ixbtGames_parse()
# # test()

def tenor():
    tenor_api_key='AIzaSyBOcqMmqBT9JD1sLs5y7K-9Q6KRbMcci3g'
    ckey='py teleg bot'
    # response = requests.get(f"https://tenor.com/search/{gifki_zapr}-gifs")
    response = requests.get(f"https://tenor.googleapis.com/v2/search?q=папич&key={tenor_api_key}&client_key={ckey}&limit=100000")
    soup=BeautifulSoup(response.text,features="html.parser")    
    
    # if response.status_code == 200:
    #         # load the GIFs using the urls for the smaller GIF sizes
    #     with open('test.json','w') as file:
    #         top_8gifs = json.dump(response.json(),file,indent=3, ensure_ascii=False)
    # else:
    #     top_8gifs = None
    # gifs = []
    # print(soup)
    # for gif in soup.findAll('img'):
    #     gifs.append(gif.get('src'))
        
    # with open('test.json') as file:
    news_list_cybersport=response.json()
    gifs = []
    for view in news_list_cybersport['results']:
        # news_cybersport=f"{(view['data'][1]['id'])}\n"
        gifs.append(view['url'])
    print(random.choice(gifs))
tenor()