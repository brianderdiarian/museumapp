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

class BrooklynSpider(Spider):
    name = "brooklynmuseumcon"
    allowed_domains = ["brooklynmuseum.org"]
    start_urls = [
        'https://www.brooklynmuseum.org/opencollection/objects?collection_id=8&object_year_begin=1850&on_view_only=1&x=9&y=18',
        'https://www.brooklynmuseum.org/opencollection/objects?offset=30&limit=30&object_year_begin=1850&on_view_only=1&collection_id=8',
        'https://www.brooklynmuseum.org/opencollection/objects?offset=60&limit=30&object_year_begin=1850&on_view_only=1&collection_id=8',
    ]


    def parse(self, response):
        # Eliminate the [2] from response.xpath to search all works on page
        #for href in response.xpath('//*[@id="works"]/div/div[2]/a/@href'):
        for href in response.xpath('/html/body/div[3]/div[5]/div/div[3]//a/@href'):    
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_artwork)

    def parse_artwork(self, response):
        global Artwork

        accession_number = "BM" + response.xpath('//strong[contains(text(), "ACCESSION NUMBER")]/parent::div[1]/text()').extract()[1].strip()

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
            try:
                artist = response.xpath('/html/body/div[3]/div[1]/div[2]/div[2]/h3/text()').extract()[0].strip()
                artist_sans_accents = remove_accents(artist)
            except:
                artist = response.xpath('/html/body/div[3]/div[1]/div[2]/div[6]/a/text()').extract()[0].strip()
                artist_sans_accents = remove_accents(artist)

            title = response.xpath('/html/body/div[3]/div[1]/div[2]/div[1]/h1/text()').extract()[0].strip()

            title_sans_accents = remove_accents(title)

            date = response.xpath('//strong[contains(text(), "DATES")]/parent::div[1]/text()').extract()[1].strip()

            medium = response.xpath('//strong[contains(text(), "MEDIUM")]/parent::div[1]/text()').extract()[1].strip()

            description = "None"

            dimensions = response.xpath('//strong[contains(text(), "DIMENSIONS")]/parent::div[1]/text()').extract()[1].strip()
            
            collection = Collection.objects.get(collection_name__contains="Brooklyn Museum")
            
            pageurl = response.request.url

            try:
                imageurl = response.xpath('/html/body/div[3]/div[1]/div[1]/div/div/div[1]/div/img/@src').extract()[0]
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