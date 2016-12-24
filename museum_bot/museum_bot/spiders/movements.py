import scrapy
import datetime
import json
import os

from museum_project.settings import BASE_DIR
from scrapy.spiders import Spider
from museum_bot.items import ArtistItem

class MetSpider(Spider):
    name = "artists"
    allowed_domains = []
    start_urls = [
        'https://en.wikipedia.org/wiki/List_of_art_movements',
    ]


    def parse(self, response):


        #movement =


        yield MovementItem(
            movement=movement
        )