import scrapy
import datetime
import json
import os
import time

from museum_project.settings import BASE_DIR
from scrapy.spiders import Spider
from museum_bot.items import ArtworkItem, DisplayItem, ArtistItem
from app.tools import strip_parenthesis, cleanhtml
from app.tools import remove_accents, today, yesterday
from app.models import Artwork, Artist, Collection, NameVariant, Display, LastCrawl
from scrapy import signals

if LastCrawl.objects.get(spider_name="nyguggenheim").last_crawled != today:

    class GugSpider(Spider):
        name = "nyguggenheim"
        allowed_domains = ["guggenheim.org"]
        start_urls = [
            'https://www.guggenheim.org/wp-json/wp/v2/artwork?filter%5Bcategory_name%5D=on-view-in-new-york&per_page=100',
        ]

        def parse(self, response):

            results = json.loads(response.body_as_unicode())

            global Artwork

            for result in results:

                accession_number = "NYGUG" + result['accession']

                if Display.objects.filter(artwork__accession_number=accession_number).filter(end_date=yesterday).exists():
                    Display.objects.filter(artwork__accession_number=accession_number).filter(end_date=yesterday).update(end_date=today)

                elif Display.objects.filter(artwork__accession_number=accession_number).exists():

                    collection = Collection.objects.get(collection_name__contains="Guggenheim")

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
                    if result['artist'][0]['name'] == " ":
                        artist = "Unknown"
                        artist_sans_accents = "Unknown"
                    else:    
                        artist = result['artist'][0]['name']
                        artist_sans_accents = remove_accents(artist)
             
                    title = result['title']['rendered']

                    title_sans_accents = remove_accents(title)
                 
                    date = result['dates']
                 
                    medium = result['medium']
                 
                    description = cleanhtml(result['content']['rendered'])
                 
                    dimensions = result['dimensions']

                    collection = Collection.objects.get(collection_name__contains="Guggenheim")
                 
                    try:
                        imageurl = result['featured_image']['src']
                    except:
                        imageurl = "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"

                    pageurl =  result['link']

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

        @classmethod
        def from_crawler(cls, crawler, *args, **kwargs):
            spider = super(GugSpider, cls).from_crawler(crawler, *args, **kwargs)
            # crawler.signals.connect(spider.spider_opened, signals.spider_opened)
            crawler.signals.connect(spider.spider_closed, signals.spider_closed)
            return spider

        # def spider_opened(self, spider):

        def spider_closed(self, spider):
            LastCrawl.objects.filter(spider_name="brooklynmuseumamerican").update(last_crawled=today)