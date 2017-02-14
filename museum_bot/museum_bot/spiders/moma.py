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
    name = "moma"
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

        if Display.objects.filter(artwork__accession_number=accession_number).filter(end_date=yesterday).exists():
            Display.objects.filter(artwork__accession_number=accession_number).filter(end_date=yesterday).update(end_date=today)

        elif Display.objects.filter(artwork__accession_number=accession_number).exists():

            collection = Collection.objects.get(collection_name__contains="MoMA")

            artwork = Artwork.objects.get(accession_number=accession_number)

            start_date = datetime.date.today().isoformat()

            end_date = datetime.date.today().isoformat()

            yield DisplayItem(
                collection = collection,
                artwork = artwork,
                start_date = start_date,
                end_date = end_date,
            )

        else:

            artist = response.xpath('/html/body/div[3]/div/div/div[1]/div/div/h2/a/text()').extract()[0].strip()

            artist_sans_accents = remove_accents(artist)

            try:
                title = response.xpath('/html/body/div[3]/div/div/div[1]/div/div/h1/em/text()').extract()[0].strip()
            except:
                title = response.xpath('/html/body/div[3]/div/div/div[1]/div/div/h1/text()').extract()[0].strip()

            title_sans_accents = remove_accents(title)

            date = response.xpath('/html/body/div[3]/div/div/div[1]/div/div/h3/text()').extract()[0].strip()

            medium = response.xpath('//*[contains(text(), "Medium")]/following-sibling::dd[1]/text()').extract()[0].strip()
     
            try:
                description = response.xpath('/html/body/div[3]/div[1]/section[2]/div/div[2]/div[1]/p[1]/text()').extract()[0].strip()
            except:
                description = "None"

            dimensions = response.xpath('//*[contains(text(), "Dimensions")]/following-sibling::dd[1]/text()').extract()[0].strip()

            collection = Collection.objects.get(collection_name__contains="MoMA")

            pageurl = response.request.url
            
            try:
                image = response.xpath('/html/body/div[3]/div/div/div[1]/section[1]/div/img/@srcset[1]').extract()[0].split(',')[0].strip('320w').strip()
                imagestripped = str(image)
                imageurl = 'http://www.moma.org'+imagestripped
            except:
                imageurl = "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"
             
            timestamp = datetime.date.today().isoformat()

            start_date = datetime.date.today().isoformat()

            end_date = datetime.date.today().isoformat()
            
            try:
                artist = NameVariant.objects.get(name=artist_sans_accents).artist
            except:
                try:
                    artist = Artist.objects.get(artist_sans_accents=artist_sans_accents)
                except:
                    artist = artist_sans_accents
                    yield ArtistItem(
                        artist_sans_accents=artist_sans_accents,
                    )
                    time.sleep(2)
                    artist = Artist.objects.get(artist_sans_accents=artist_sans_accents)

            yield ArtworkItem(
                title=title,
                title_sans_accents=title_sans_accents,
                date=date,
                medium=medium,
                description=description,
                dimensions=dimensions,
                collection=collection,
                imageurl=imageurl,
                pageurl=pageurl,
                accession_number=accession_number,
                timestamp=timestamp,
                artist=artist,
            )

            from app.models import Artwork

            artwork = Artwork.objects.get(accession_number=accession_number)

            yield DisplayItem(
                collection = collection,
                artwork = artwork,
                start_date = start_date,
                end_date = end_date,
            )