import json
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def cybersport_parse():
        response = requests.get(f"https://www.cybersport.ru/tags/games")
        soup=BeautifulSoup(response.text,features="lxml")
        link_CocWY=soup.find_all("a",class_="link_CocWY")

        news_dict_cybersport = {}
        for article in link_CocWY:
                article_title = article.find('h3', class_="title_nSS03").text.strip()
                article_url=f'https://www.cybersport.ru{article.get("href")}'
                
                article_data_time = article.find("time").get("datetime")
                date_from_iso = datetime.fromisoformat(article_data_time)
                date_time=datetime.strftime(date_from_iso,"%Y-%m-%d %H:%M:%S")
                article_data_timestamp=time.mktime(datetime.strptime(date_time,"%Y-%m-%d %H:%M:%S").timetuple())
                
                article_id = article_url.split('/')[-1]
                # article_id =article_id[:4]
                
                # print(f'{article_title} | {article_url} | {article_data_timestamp}')
                # print(f'{article_data_timestamp}')
                news_dict_cybersport[article_id] = {
                        "article_data_timestamp" : article_data_timestamp,
                        "article_title" : article_title,
                        "article_url" : article_url
                }
        with open('news_cybersport.json','w') as file:
                json.dump(news_dict_cybersport,file,indent=3, ensure_ascii=False)
        # print(link_CocWY)
        # gifs = []
        # soup.findAll()
        # for gif in soup.findAll('img'):
        #     gifs.append(gif.get('src'))
        
def check_news_cybersport_update():
        with open('website_parse_json/news_cybersport.json') as file:
                news_list_cybersport=json.load(file)

        response = requests.get(f"https://www.cybersport.ru/tags/games")
        soup=BeautifulSoup(response.text,features="lxml")
        link_CocWY=soup.find_all("a",class_="link_CocWY")
        
        fresh_news_cybersport={}       
        for article in link_CocWY:
                article_url=f'https://www.cybersport.ru{article.get("href")}'
                article_id = article_url.split('/')[-1]
                if article_id in news_list_cybersport:
                        continue
                else:
                        article_title = article.find('h3', class_="title_nSS03").text.strip()
        
                        article_data_time = article.find("time").get("datetime")
                        date_from_iso = datetime.fromisoformat(article_data_time)
                        date_time=datetime.strftime(date_from_iso,"%Y-%m-%d %H:%M:%S")
                        article_data_timestamp=time.mktime(datetime.strptime(date_time,"%Y-%m-%d %H:%M:%S").timetuple())
        
                        article_id = article_url.split('/')[-1]

                        news_list_cybersport[article_id] = {
                                "article_data_timestamp" : article_data_timestamp,
                                "article_title" : article_title,
                                "article_url" : article_url
                        }
                        fresh_news_cybersport[article_id] = {
                                "article_data_timestamp" : article_data_timestamp,
                                "article_title" : article_title,
                                "article_url" : article_url
                        }

        with open('website_parse_json/news_cybersport.json','w') as file:
                json.dump(news_list_cybersport,file,indent=3, ensure_ascii=False)
        return fresh_news_cybersport

# check_news_cybersport_update()
# cybersport_parse()

