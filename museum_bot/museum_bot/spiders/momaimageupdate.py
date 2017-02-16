import scrapy
import datetime
import json
import os
import time

from museum_project.settings import BASE_DIR
from scrapy.spiders import Spider
from museum_bot.items import ArtworkItem, DisplayItem, ArtistItem
from app.tools import remove_accents, yesterday, today
from app.models import Artwork, Artist, Collection, NameVariant, Display

class MomaSpider(Spider):
    name = "momaimageupdate"
    allowed_domains = ["moma.org"]
    start_urls = [
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=2&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=3&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=4&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=5&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=6&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=7&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=8&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=9&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=10&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=11&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=12&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=13&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=14&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=15&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=16&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=17&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=18&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=19&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=20&direction=fwd',
    ]


    def parse(self, response):

        for href in response.xpath('//*[@id="works"]/div/div/a/@href'):    
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_artwork)

    def parse_artwork(self, response):
        global Artwork
        
        accession_number = "MOMA" + response.xpath('//*[contains(text(), "Object number")]/following-sibling::dd[1]/text()').extract()[0].strip()

        if Artwork.objects.filter(accession_number=accession_number).exists():

            try:
                image = response.xpath('/html/body/div[3]/div/div/div[1]/section[1]/div/img/@srcset[1]').extract()[0].split(',')[0].strip('320w').strip()
                imagestripped = str(image)
                imageurl = 'http://www.moma.org'+imagestripped
            except:
                imageurl = "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"

            Artwork.objects.filter(accession_number=accession_number).update(imageurl=imageurl)

        else:
            pass