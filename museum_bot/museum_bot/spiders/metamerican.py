import scrapy
import datetime
import json
import os
import itertools
import time

from app.models import Artwork, Artist, Collection, NameVariant
from museum_project.settings import BASE_DIR
from scrapy.spiders import Spider
from museum_bot.items import ArtworkItem, DisplayItem, ArtistItem
from app.tools import strip_parenthesis
from app.tools import remove_accents
from w3lib.html import remove_tags

class MetSpider(Spider):
    name = "metamerican"
    allowed_domains = ["metmuseum.org"]
    start_urls = [
        'http://www.metmuseum.org/api/collection/collectionlisting?artist=&department=2&era=&geolocation=&material=&offset=0&pageSize=0&perPage=100&showOnly=onDisplay&sortBy=Relevance&sortOrder=asc',
        'http://www.metmuseum.org/api/collection/collectionlisting?artist=&department=2&era=&geolocation=&material=&offset=100&pageSize=0&perPage=100&showOnly=onDisplay&sortBy=Relevance&sortOrder=asc',
        'http://www.metmuseum.org/api/collection/collectionlisting?artist=&department=2&era=&geolocation=&material=&offset=200&pageSize=0&perPage=100&showOnly=onDisplay&sortBy=Relevance&sortOrder=asc',
        'http://www.metmuseum.org/api/collection/collectionlisting?artist=&department=2&era=&geolocation=&material=&offset=300&pageSize=0&perPage=100&showOnly=onDisplay&sortBy=Relevance&sortOrder=asc',
        'http://www.metmuseum.org/api/collection/collectionlisting?artist=&department=2&era=&geolocation=&material=&offset=400&pageSize=0&perPage=100&showOnly=onDisplay&sortBy=Relevance&sortOrder=asc',
        'http://www.metmuseum.org/api/collection/collectionlisting?artist=&department=2&era=&geolocation=&material=&offset=500&pageSize=0&perPage=100&showOnly=onDisplay&sortBy=Relevance&sortOrder=asc',
        'http://www.metmuseum.org/api/collection/collectionlisting?artist=&department=2&era=&geolocation=&material=&offset=600&pageSize=0&perPage=100&showOnly=onDisplay&sortBy=Relevance&sortOrder=asc',
        'http://www.metmuseum.org/api/collection/collectionlisting?artist=&department=2&era=&geolocation=&material=&offset=700&pageSize=0&perPage=100&showOnly=onDisplay&sortBy=Relevance&sortOrder=asc',
        'http://www.metmuseum.org/api/collection/collectionlisting?artist=&department=2&era=&geolocation=&material=&offset=800&pageSize=0&perPage=100&showOnly=onDisplay&sortBy=Relevance&sortOrder=asc',
        'http://www.metmuseum.org/api/collection/collectionlisting?artist=&department=2&era=&geolocation=&material=&offset=900&pageSize=0&perPage=100&showOnly=onDisplay&sortBy=Relevance&sortOrder=asc',
        'http://www.metmuseum.org/api/collection/collectionlisting?artist=&department=2&era=&geolocation=&material=&offset=1000&pageSize=0&perPage=100&showOnly=onDisplay&sortBy=Relevance&sortOrder=asc',
        'http://www.metmuseum.org/api/collection/collectionlisting?artist=&department=2&era=&geolocation=&material=&offset=1100&pageSize=0&perPage=100&showOnly=onDisplay&sortBy=Relevance&sortOrder=asc',
        'http://www.metmuseum.org/api/collection/collectionlisting?artist=&department=2&era=&geolocation=&material=&offset=1200&pageSize=0&perPage=100&showOnly=onDisplay&sortBy=Relevance&sortOrder=asc',
    ]


    def parse(self, response):
        # Eliminate the [2] from response.xpath to search all works on page
        #for href in response.xpath('//*[@id="works"]/div/div[2]/a/@href'):
        jsonresponse = json.loads(response.body_as_unicode())

        results = jsonresponse['results']

        for result in results:

            if result['description'] == " ":
                artist = "Unknown Artist"
                artist_sans_accents = "Unknown Artist"
            elif result['description'] == "Unknown":
                artist = "Unknown Artist"
                artist_sans_accents = "Unknown Artist"
            else:    
                artist = strip_parenthesis(result['description'].replace("&#39;","'")).strip()
                artist_sans_accents = remove_accents(artist)
                artist_sans_accents = artist_sans_accents.replace(',','')
         
            title = result['title'].replace("&#39;","'")

            title_sans_accents = remove_accents(title)
         
            try:
                date = result['date']
            except:
                date = "Date Unknown"
         
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

            accession_number = "MET" + result['accessionNumber']
         
            timestamp = datetime.date.today().isoformat()

            #artistlist = list(Artist.objects.values_list('artist_sans_accents', flat=True))
            # for i, s in enumerate(artistlist):
            #     artistlist[i] = s.split(',')
            # artistlist = list(itertools.chain.from_iterable(artistlist))

            # artistlist = [x.strip(' ') for x in artistlist]
                
            # if any(artist_sans_accents == x for x in artistlist):
            #     pass
            # else:
            #     yield ArtistItem(
            #         artist_sans_accents=artist_sans_accents,
            #     )

            # artist = Artist.objects.get(artist_sans_accents__contains=artist_sans_accents)
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
                    artist = Artist.objects.get(artist_sans_accents=artist_sans_accents).earliest()

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
            )