import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
from lxml import html
from latest_user_agents import get_latest_user_agents, get_random_user_agent
import time 
import logging

def main():
    #get request from top 250 films site
    logging.basicConfig(filename="newfile.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.debug("get top 250 movies from imdb")
    response = requests.get('https://www.imdb.com/chart/top')
    soup = BeautifulSoup(response.content, 'html.parser')
    ids = soup.select('td.titleColumn')
    movies = []

    #loop to get movies
    for i in range(len(ids)):
        try:
            movies.append(get_by_id(ids[i].a['href']))
            logger.debug(f"get {ids[i].text} info")
            print(i)
        except:
            logger.debug(f"error {ids[i].text}")
            continue
    with open('movies.json', 'w', encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)
    return movies

#function to get movies info
def get_by_id(id):
    #create random header
    headers = {'User-Agent': get_random_user_agent()}
    #get request
    response = requests.get('https://www.imdb.com' + id,headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    #parse data
    header_data = soup.find('script',{"type" : "application/ld+json"})
    result = json.loads(header_data.find(text=True))
    top_casts = soup.find_all('div', {"class":"sc-bfec09a1-7 iDmJtd"})
    detail = soup.find('div', {"data-testid" : "title-details-section"})
    try:
        box_office = soup.find('div',{"data-testid":"title-boxoffice-section"}) 
        output = {
        "type": result.get('@type'),
        "name": result.get('name'),
        "url": result.get('url'),
        "poster": result.get('image'),
        "description": result.get('description'),
        "review": {
            "author": result.get("review", {'author': {'name': None}}).get('author').get('name'),
            "dateCreated": result.get("review", {"dateCreated": None}).get("dateCreated"),
            "inLanguage": result.get("review", {"inLanguage": None}).get("inLanguage"),
            "heading": result.get("review", {"name": None}).get("name"),
            "reviewBody": result.get("review", {"reviewBody": None}).get("reviewBody"),
            "reviewRating": {
                "worstRating": result.get("review", {"reviewRating": {"worstRating": None}})
                    .get("reviewRating",{"worstRating": None}).get("worstRating"),
                "bestRating": result.get("review", {"reviewRating": {"bestRating": None}})
                    .get("reviewRating",{"bestRating": None}).get("bestRating"),
                "ratingValue": result.get("review", {"reviewRating": {"ratingValue": None}})
                    .get("reviewRating",{"ratingValue": None}).get("ratingValue"),
            },
        },
        "rating": {
            "ratingCount": result.get("aggregateRating", {"ratingCount": None}).get("ratingCount"),
            "bestRating": result.get("aggregateRating", {"bestRating": None}).get("bestRating"),
            "worstRating": result.get("aggregateRating", {"worstRating": None}).get("worstRating"),
            "ratingValue": result.get("aggregateRating", {"ratingValue": None}).get("ratingValue"),
        },
        "contentRating": result.get("contentRating"),
        "genre": result.get("genre"),
        "datePublished": result.get("datePublished"),
        "keywords": result.get("keywords"),
        "duration": result.get("duration"),
        "actor": [
            {"name": actor.get("name"), "url": actor.get("url")} for actor in result.get("actor", [])
        ],
        "director": [
            {"name": director.get("name"), "url": director.get("url")} for director in result.get("director", [])
        ],
        "creator": [
            {"name": creator.get("name"), "url": creator.get("url")} for creator in result.get("creator", [])
            if creator.get('@type') == 'Person'
        ],
        "top casts": [{"actor" : cast.a.text,
             "characters": list(map(lambda x: x.text,cast.find_all('li')))} for cast in top_casts],
        "Release date": detail.find('li',{"data-testid":"title-details-releasedate"}).find('a',{"class":"ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"}).text,
        "country" : detail.find('li',{"data-testid":"title-details-origin"}).find('a',{"class":"ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"}).text,
        "box_office": [{item.find('button').text : item.find('div').text} for item in box_office.find_all('li', {"class":"ipc-metadata-list__item sc-6d4f3f8c-2 fJEELB"})]
    }
    except:
        output = {
        "type": result.get('@type'),
        "name": result.get('name'),
        "url": result.get('url'),
        "poster": result.get('image'),
        "description": result.get('description'),
        "review": {
            "author": result.get("review", {'author': {'name': None}}).get('author').get('name'),
            "dateCreated": result.get("review", {"dateCreated": None}).get("dateCreated"),
            "inLanguage": result.get("review", {"inLanguage": None}).get("inLanguage"),
            "heading": result.get("review", {"name": None}).get("name"),
            "reviewBody": result.get("review", {"reviewBody": None}).get("reviewBody"),
            "reviewRating": {
                "worstRating": result.get("review", {"reviewRating": {"worstRating": None}})
                    .get("reviewRating",{"worstRating": None}).get("worstRating"),
                "bestRating": result.get("review", {"reviewRating": {"bestRating": None}})
                    .get("reviewRating",{"bestRating": None}).get("bestRating"),
                "ratingValue": result.get("review", {"reviewRating": {"ratingValue": None}})
                    .get("reviewRating",{"ratingValue": None}).get("ratingValue"),
            },
        },
        "rating": {
            "ratingCount": result.get("aggregateRating", {"ratingCount": None}).get("ratingCount"),
            "bestRating": result.get("aggregateRating", {"bestRating": None}).get("bestRating"),
            "worstRating": result.get("aggregateRating", {"worstRating": None}).get("worstRating"),
            "ratingValue": result.get("aggregateRating", {"ratingValue": None}).get("ratingValue"),
        },
        "contentRating": result.get("contentRating"),
        "genre": result.get("genre"),
        "datePublished": result.get("datePublished"),
        "keywords": result.get("keywords"),
        "duration": result.get("duration"),
        "actor": [
            {"name": actor.get("name"), "url": actor.get("url")} for actor in result.get("actor", [])
        ],
        "director": [
            {"name": director.get("name"), "url": director.get("url")} for director in result.get("director", [])
        ],
        "creator": [
            {"name": creator.get("name"), "url": creator.get("url")} for creator in result.get("creator", [])
            if creator.get('@type') == 'Person'
        ],
        "top casts": [{"actor" : cast.a.text,
             "characters": list(map(lambda x: x.text,cast.find_all('li')))} for cast in top_casts],
        "Release date": detail.find('li',{"data-testid":"title-details-releasedate"}).find('a',{"class":"ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"}).text,
        "country" : detail.find('li',{"data-testid":"title-details-origin"}).find('a',{"class":"ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"}).text,
        "box_office": None
    }
    return output

if __name__ == "__main__":
    main()