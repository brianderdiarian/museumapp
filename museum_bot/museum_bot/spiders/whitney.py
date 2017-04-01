import scrapy
import datetime
import json
import os
import itertools
import time

from app.models import Artwork, Artist, Collection, NameVariant, Display, LastCrawl
from museum_project.settings import BASE_DIR
from scrapy.spiders import Spider
from museum_bot.items import ArtworkItem, DisplayItem, ArtistItem
from app.tools import strip_parenthesis
from app.tools import remove_accents, yesterday, today
from w3lib.html import remove_tags

if LastCrawl.objects.get(spider_name="whitney").last_crawled != today:

    class MetSpider(Spider):
        name = "whitney"
        allowed_domains = ["http://collection.whitney.org/"]
        start_urls = [
            'http://collection.whitney.org/json/groups/5/?page=1&format=json',
            'http://collection.whitney.org/json/groups/5/?page=2&format=json',
            'http://collection.whitney.org/json/groups/5/?page=3&format=json',
            'http://collection.whitney.org/json/groups/5/?page=4&format=json',
            'http://collection.whitney.org/json/groups/5/?page=5&format=json',
            'http://collection.whitney.org/json/groups/5/?page=6&format=json',
            'http://collection.whitney.org/json/groups/5/?page=7&format=json',
            'http://collection.whitney.org/json/groups/5/?page=8&format=json',
            'http://collection.whitney.org/json/groups/5/?page=9&format=json',
            'http://collection.whitney.org/json/groups/5/?page=10&format=json',
            'http://collection.whitney.org/json/groups/5/?page=11&format=json',
            'http://collection.whitney.org/json/groups/5/?page=12&format=json',
        ]

        def parse(self, response):
            global Artwork

            jsonresponse = json.loads(response.body_as_unicode())

            results = jsonresponse['group_objects']['results']

            
            for result in results:
                try:
                    accession_number = "WHIT" + result['accession_number']

                    if Display.objects.filter(artwork__accession_number=accession_number).filter(end_date=today).exists():
                        continue

                    elif Display.objects.filter(artwork__accession_number=accession_number).filter(end_date=yesterday).exists():
                        Display.objects.filter(artwork__accession_number=accession_number).filter(end_date=yesterday).update(end_date=today)

                    elif Display.objects.filter(artwork__accession_number=accession_number).exists():

                        collection = Collection.objects.get(collection_name__contains="Whitney")

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
                        if result['artist_name'] == " ":
                            artist = "Unknown Artist"
                            artist_sans_accents = "Unknown Artist"
                        elif result['artist_name'] == "Unknown":
                            artist = "Unknown Artist"
                            artist_sans_accents = "Unknown Artist"
                        else:    
                            artist = strip_parenthesis(result['artist_name'].replace("&#39;","'")).strip()
                            artist_sans_accents = remove_accents(artist)
                            artist_sans_accents = artist_sans_accents.replace(',','')
                     
                        title = result['title'].replace("&#39;","'")

                        title_sans_accents = remove_accents(title)
                     
                        try:
                            date = result['display_date']
                        except:
                            date = "Date Unknown"
                     
                        #medium = result['medium']
                     
                        description = "None"
                     
                        dimensions = "None"

                        collection = Collection.objects.get(collection_name__contains="Whitney")
                     
                        try:
                            if result['primary_image_id'] == 0:
                                imageurl = "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"
                            else:
                                imageurl = "http://collectionimages.whitney.org/standard/" + str(result['primary_image_id']) + "/listing.jpg"
                        except:
                            imageurl = "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"

                        pageurl = "http://collection.whitney.org/object/" + str(result['object_id'])
                     
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
                            #medium=medium,
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
                except:
                    continue

    LastCrawl.objects.filter(spider_name="whitney").update(last_crawled=today)