import scrapy
import datetime
import json
import os
import time

from museum_project.settings import BASE_DIR
from scrapy.spiders import Spider
from museum_bot.items import ArtworkItem, DisplayItem, ArtistItem
from app.tools import strip_parenthesis, cleanhtml
from app.tools import remove_accents
from app.models import Artwork, Artist, Collection, NameVariant

class MetSpider(Spider):
    name = "nyguggenheim"
    allowed_domains = ["guggenheim.org"]
    start_urls = [
        'https://www.guggenheim.org/wp-json/wp/v2/artwork?filter%5Bcategory_name%5D=on-view-in-new-york&per_page=100',
    ]


    def parse(self, response):

        results = json.loads(response.body_as_unicode())

        for result in results:

            artist = result['artist'][0]['name']

            artist_sans_accents = remove_accents(artist)
         
            title = result['title']['rendered']

            title_sans_accents = remove_accents(title)
         
            date = result['dates']
         
            medium = result['medium']
         
            description = cleanhtml(result['content']['rendered'])
         
            dimensions = result['dimensions']
         
            collection = "Solomon R. Guggenheim Museum"

            collection = Collection.objects.get(collection_name__contains=collection)
         
            try:
                imageurl = result['featured_image']['src']
            except:
                imageurl = "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"

            pageurl =  result['link']

            accession_number = "NYGUG" + result['accession']
         
            timestamp = datetime.date.today().isoformat()

            artistlist = Artist.objects.values_list('artist_sans_accents', flat=True)
                
            if any(artist_sans_accents in x for x in artistlist):
                pass
            else:
                yield ArtistItem(
                    artist_sans_accents=artist_sans_accents,
                )

            artist = Artist.objects.get(artist_sans_accents__contains=artist_sans_accents)    

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