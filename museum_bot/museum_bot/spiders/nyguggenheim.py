import scrapy
import datetime
import json
import os

from museum_project.settings import BASE_DIR
from scrapy.spiders import Spider
from museum_bot.items import ArtworkItem
from app.tools import strip_parenthesis, cleanhtml
from app.tools import remove_accents

class MetSpider(Spider):
    name = "nyguggenheim"
    allowed_domains = ["guggenheim.org"]
    start_urls = [
        'https://www.guggenheim.org/wp-json/wp/v2/artwork?filter%5Bcategory_name%5D=on-view-in-new-york&per_page=100',
    ]


    def parse(self, response):
        # Eliminate the [2] from response.xpath to search all works on page
        #for href in response.xpath('//*[@id="works"]/div/div[2]/a/@href'):
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
         
            collection = "On View at the Solomon R. Guggenheim Museum"
         
            coordinates = "40.782975°N 73.958992°W﻿"
            try:
                imageurl = result['featured_image']['src']
            except:
                imageurl = "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"

            pageurl =  result['link']

            accession_number = "NYGUG" + result['accession']
         
            timestamp = datetime.date.today().isoformat()

            address = "1071 5th Ave, New York, NY 10128"

            with open(os.path.join(BASE_DIR,'app/artist_list.json')) as json_data:
                stats=json.load(json_data)

            for a in stats:
                if artist_sans_accents in a['Artist']:
                    sex = a['Sex']
                    born = a['Born']
                    died = a['Died']
                    movements = a['Movement(s)']
                    descriptors = a['Descriptors']
                    nationality = a['Nationality']
                    break
                else:
                    sex = ""
                    born = ""
                    died = ""
                    movements = ""
                    descriptors = ""
                    nationality = ""

            yield ArtworkItem(
                artist=artist,
                artist_sans_accents=artist_sans_accents,
                title=title,
                title_sans_accents=title_sans_accents,
                date=date,
                medium=medium,
                description=description,
                dimensions=dimensions,
                collection=collection,
                coordinates=coordinates,
                imageurl=imageurl,
                pageurl=pageurl,
                accession_number=accession_number,
                timestamp=timestamp,
                address=address,
                sex=sex,
                born=born,
                died=died,
                movements=movements,
                descriptors=descriptors,
                nationality=nationality,
            )