import scrapy
import datetime
import json
import os
import time

from museum_project.settings import BASE_DIR
from scrapy.spiders import Spider
from museum_bot.items import ArtworkItem, DisplayItem, ArtistItem
from app.tools import remove_accents, yesterday, today, skipcatch
from app.models import Artwork, Artist, Collection, NameVariant, Display, LastCrawl

if LastCrawl.objects.get(spider_name="frickpainting").last_crawled != today:

    class BrooklynSpider(Spider):
        name = "frickpainting"
        allowed_domains = ["collections.frick.org"]
        start_urls = [
            'http://collections.frick.org/view/objects/asitem/152/1/',
        ]

        def parse(self, response):
            global Artwork

            if response.xpath('//*[@id="onview"]/span/text()').extract()[0].strip() == 'Currently on View':

                accession_number = "FR" + response.xpath('string(//body)').re(r"\d{4}[.]\d[.]\d+")[0].strip()

                if Display.objects.filter(artwork__accession_number=accession_number).filter(end_date__gte=skipcatch).exists():
                    Display.objects.filter(artwork__accession_number=accession_number).filter(end_date__gte=skipcatch).update(end_date=today)

                    next_page = response.xpath('//*[@id="pagenav"]/div[contains(@class,"pagenavright")]//@href').extract()[0]
                    if next_page is not None:
                        next_page = response.urljoin(next_page)
                        yield scrapy.Request(next_page, callback=self.parse)

                elif Display.objects.filter(artwork__accession_number=accession_number).exists():

                    collection = Collection.objects.get(collection_name__contains="Frick")

                    artwork = Artwork.objects.get(accession_number=accession_number)

                    start_date = datetime.date.today().isoformat()

                    end_date = datetime.date.today().isoformat()

                    yield DisplayItem(
                        collection = collection,
                        artwork = artwork,
                        start_date = start_date,
                        end_date = end_date,
                    )
                        
                    next_page = response.xpath('//*[@id="pagenav"]/div[contains(@class,"pagenavright")]//@href').extract()[0]
                    if next_page is not None:
                        next_page = response.urljoin(next_page)
                        yield scrapy.Request(next_page, callback=self.parse)
                
                else:
                    artist = response.xpath('.//span[contains(@class, "artistName")]/text()').extract()[0].strip()
                    artist_sans_accents = remove_accents(artist)

                    title = response.xpath('//*[@id="viewForm"]//em/text()').extract()[0].strip()

                    title_sans_accents = remove_accents(title)

                    # date = response.xpath('//strong[contains(text(), "DATES")]/parent::div[1]/text()').extract()[1].strip()

                    # medium = response.xpath('//strong[contains(text(), "MEDIUM")]/parent::div[1]/text()').extract()[1].strip()

                    description = "None"

                    #dimensions = response.xpath('//strong[contains(text(), "DIMENSIONS")]/parent::div[1]/text()').extract()[1].strip()
                    
                    collection = Collection.objects.get(collection_name__contains="Frick")
                    
                    pageurl = response.request.url

                    try:
                        imageurl = "http://collections.frick.org" + response.xpath('//*[@id="singlemedia"]//img/@src').extract()[0]
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
                        #date=date,
                        #medium=medium,
                        description=description,
                        #dimensions=dimensions,
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

                    next_page = response.xpath('//*[@id="pagenav"]/div[contains(@class,"pagenavright")]//@href').extract()[0]
                    if next_page is not None:
                        next_page = response.urljoin(next_page)
                        yield scrapy.Request(next_page, callback=self.parse)
                
            else:
                next_page = response.xpath('//*[@id="pagenav"]/div[contains(@class,"pagenavright")]//@href').extract()[0]
                if next_page is not None:
                    next_page = response.urljoin(next_page)
                    yield scrapy.Request(next_page, callback=self.parse)

    LastCrawl.objects.filter(spider_name="frickpainting").update(last_crawled=today)