import scrapy
import datetime
import json
import os
import time

from app.models import Artwork, Artist, Collection, NameVariant, Display
from museum_project.settings import BASE_DIR
from scrapy.spiders import Spider
from museum_bot.items import ArtworkItem, DisplayItem, ArtistItem
from app.tools import strip_parenthesis
from app.tools import remove_accents, yesterday, today
from w3lib.html import remove_tags

class MetSpider(Spider):
    name = "metphoto"
    allowed_domains = ["metmuseum.org"]
    start_urls = [
        'http://www.metmuseum.org/api/collection/collectionlisting?artist=&department=19&era=&geolocation=&material=&offset=0&pageSize=0&perPage=100&showOnly=onDisplay&sortBy=Relevance&sortOrder=asc',
        'http://www.metmuseum.org/api/collection/collectionlisting?artist=&department=19&era=&geolocation=&material=&offset=100&pageSize=0&perPage=100&showOnly=onDisplay&sortBy=Relevance&sortOrder=asc',
        'http://www.metmuseum.org/api/collection/collectionlisting?artist=&department=19&era=&geolocation=&material=&offset=200&pageSize=0&perPage=100&showOnly=onDisplay&sortBy=Relevance&sortOrder=asc',
        'http://www.metmuseum.org/api/collection/collectionlisting?artist=&department=19&era=&geolocation=&material=&offset=300&pageSize=0&perPage=100&showOnly=onDisplay&sortBy=Relevance&sortOrder=asc',
        'http://www.metmuseum.org/api/collection/collectionlisting?artist=&department=19&era=&geolocation=&material=&offset=400&pageSize=0&perPage=100&showOnly=onDisplay&sortBy=Relevance&sortOrder=asc',
        'http://www.metmuseum.org/api/collection/collectionlisting?artist=&department=19&era=&geolocation=&material=&offset=500&pageSize=0&perPage=100&showOnly=onDisplay&sortBy=Relevance&sortOrder=asc',
        'http://www.metmuseum.org/api/collection/collectionlisting?artist=&department=19&era=&geolocation=&material=&offset=600&pageSize=0&perPage=100&showOnly=onDisplay&sortBy=Relevance&sortOrder=asc',
    ]


    def parse(self, response):
        global Artwork

        jsonresponse = json.loads(response.body_as_unicode())

        results = jsonresponse['results']

        for result in results:

            accession_number = "MET" + result['accessionNumber']

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
                if result['description'] == " ":
                    artist = "Unknown"
                    artist_sans_accents = "Unknown"
                else:    
                    artist = strip_parenthesis(result['description'].replace("&#39;","'")).strip()
                    artist_sans_accents = remove_accents(artist)
             
                title = result['title'].replace("&#39;","'")

                title_sans_accents = remove_accents(title)
             
                date = result['date']
             
                medium = result['medium']
             
                description = "None"
             
                dimensions = "None"
             
                collection = remove_tags(result['galleryInformation'])

                if "Fifth" in collection:
                    collection = Collection.objects.get(collection_name__contains="Fifth")
                else:
                    collection = Collection.objects.get(collection_name__contains="Breuer")
                
                try:
                    if result['image'] == "/content/img/placeholders/NoImageAvailableIcon.png":
                        imageurl = "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"
                    else:
                        imageurl = result['image']
                except:
                    imageurl = "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"

                pageurl = "http://www.metmuseum.org" + result['url']
             
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