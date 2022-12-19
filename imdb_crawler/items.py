# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    rating = scrapy.Field()
    year = scrapy.Field()
    user_rating = scrapy.Field()
    votes = scrapy.Field()
    metascore = scrapy.Field()
    img_url = scrapy.Field()
    countries = scrapy.Field()
    languages = scrapy.Field()
    actors  = scrapy.Field()
    genre = scrapy.Field()
    tagline = scrapy.Field()
    description = scrapy.Field()
    directors = scrapy.Field()
    runtime = scrapy.Field()
    
    pass
