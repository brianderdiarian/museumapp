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
        'file://127.0.0.1/Users/teresaderdiarian/museumapp/app/artist_list.json',
    ]


    def parse(self, response):
        # Eliminate the [2] from response.xpath to search all works on page
        #for href in response.xpath('//*[@id="works"]/div/div[2]/a/@href'):
        results = json.loads(response.body_as_unicode())

        for result in results:

            artist_sans_accents = result['Artist']
         
            born = result['Born']

            died = result['Died']
         
            movements = result['Movement(s)']
         
            descriptors = result['Descriptors']
         
            sex = result['Sex']
         
            nationality = result['Nationality']


            yield ArtistItem(
                artist_sans_accents=artist_sans_accents,
                sex=sex,
                born=born,
                died=died,
                movements=movements,
                descriptors=descriptors,
                nationality=nationality,
            )