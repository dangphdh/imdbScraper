
import pandas as pd
from bs4 import BeautifulSoup
import requests, lxml
import random 
from lxml import etree
from re import search
import json
import cloudscraper
from latest_user_agents import get_latest_user_agents, get_random_user_agent
from collections import Counter,ChainMap
import numpy as np
import threading 
import queue
import time
from fp.fp import FreeProxy
from requests_tor import RequestsTor
from sqlalchemy import create_engine


engine = create_engine('postgresql://postgres:dang1199@localhost:5432/postgres')
all_links = []
rt = RequestsTor(autochange_id=5, threads=5)
ua = get_latest_user_agents()
for i in range(1,31):
    link = f'https://masothue.com/tra-cuu-ma-so-thue-doanh-nghiep-moi-thanh-lap/?page={str(i)}'
    print(link)
    header = {"User-Agent":random.choice(ua),
              "referrer":"https://www.google.com/",
              "Connection":"keep-alive",
              "Upgrade-Insecure-Requests":"1"}
    try:
        re = rt.get(link, headers = header)
        print(re.status_code)
    except:
        re = 400
        time.sleep(20)
    if re.status_code != 200:
        rt.new_id()
        try:
            re = rt.get(link, headers = header)
            print(re.status_code)
        except:
            pass
    if re.status_code == 200:
        soup = BeautifulSoup(re.content, 'html.parser')
        lst = soup.find('div', {'class':'tax-listing'}).find_all('div')
        links = list(map(lambda x: x.a['href'],lst))
        all_links = all_links + links
got_df = pd.read_sql("select * from masothue_info", con = engine)
all_links = set(all_links)
dfs = []
for link in all_links:
    link = 'https://masothue.com' + link
    header = {"User-Agent":random.choice(ua),
              "referrer":"https://www.google.com/",
              "Connection":"keep-alive",
              "Upgrade-Insecure-Requests":"1"}
    if link in list(got_df.link):
        print('found')
    else:
        try:
            re = rt.get(link, headers = header)
            print(re.status_code)
        except:
            rt = RequestsTor(autochange_id=5, threads=5)
        if re.status_code != 200:
            try:
                rt.new_id()
                re = rt.get(link, headers = header)
                print(re.status_code)
            except:
                time.sleep(20)
                pass
        if re.status_code ==200:
            soup = BeautifulSoup(re.content, 'html.parser')
            tbl = soup.find('table',{"class":"table-taxinfo"})
            for r in tbl.find_all('td',{'colspan':'2'}):
                r.parent.decompose()
            data_frame = pd.read_html(str(tbl))[0]
            df = data_frame.transpose().reset_index(drop=True)
            df.columns = df.iloc[0]
            df.drop(df.index[0], inplace = True)
            name = tbl.find('th').text
            print(name)
            df['link'] = link
            df['Name'] = name
            dfs.append(df)
            time.sleep(2)
        else:
            continue
if len(dfs) > 0:
    df = pd.concat(dfs)
    df.to_sql('masothue_info', engine, schema ='public', if_exists = 'append')


