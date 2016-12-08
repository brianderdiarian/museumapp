import scrapy
import datetime
import json
import os

from museum_project.settings import BASE_DIR
from scrapy.spiders import Spider
from museum_bot.items import ArtworkItem
from app.tools import remove_accents

class MomaSpider(Spider):
    name = "brooklynmuseumamerican"
    allowed_domains = ["brooklynmuseum.org"]
    start_urls = [
        'https://www.brooklynmuseum.org/opencollection/objects?collection_id=9&object_year_begin=1850&on_view_only=1&x=9&y=18',
        'https://www.brooklynmuseum.org/opencollection/objects?offset=30&limit=30&object_year_begin=1850&on_view_only=1&collection_id=9',
        'https://www.brooklynmuseum.org/opencollection/objects?offset=60&limit=30&object_year_begin=1850&on_view_only=1&collection_id=9',
        'https://www.brooklynmuseum.org/opencollection/objects?offset=90&limit=30&object_year_begin=1850&on_view_only=1&collection_id=9',
        'https://www.brooklynmuseum.org/opencollection/objects?offset=120&limit=30&object_year_begin=1850&on_view_only=1&collection_id=9',
        'https://www.brooklynmuseum.org/opencollection/objects?offset=150&limit=30&object_year_begin=1850&on_view_only=1&collection_id=9',
        'https://www.brooklynmuseum.org/opencollection/objects?offset=180&limit=30&object_year_begin=1850&on_view_only=1&collection_id=9',
        'https://www.brooklynmuseum.org/opencollection/objects?offset=210&limit=30&object_year_begin=1850&on_view_only=1&collection_id=9',
        'https://www.brooklynmuseum.org/opencollection/objects?offset=240&limit=30&object_year_begin=1850&on_view_only=1&collection_id=9',
        'https://www.brooklynmuseum.org/opencollection/objects?offset=270&limit=30&object_year_begin=1850&on_view_only=1&collection_id=9',
        'https://www.brooklynmuseum.org/opencollection/objects?offset=300&limit=30&object_year_begin=1850&on_view_only=1&collection_id=9',
        'https://www.brooklynmuseum.org/opencollection/objects?offset=330&limit=30&object_year_begin=1850&on_view_only=1&collection_id=9',
        #'https://www.brooklynmuseum.org/opencollection/objects?offset=360&limit=30&object_year_begin=1850&on_view_only=1&collection_id=9',
        #'https://www.brooklynmuseum.org/opencollection/objects?offset=390&limit=30&object_year_begin=1850&on_view_only=1&collection_id=9',
        #'https://www.brooklynmuseum.org/opencollection/objects?offset=420&limit=30&object_year_begin=1850&on_view_only=1&collection_id=9',
        #'https://www.brooklynmuseum.org/opencollection/objects?offset=450&limit=30&object_year_begin=1850&on_view_only=1&collection_id=9',
        #'https://www.brooklynmuseum.org/opencollection/objects?offset=480&limit=30&object_year_begin=1850&on_view_only=1&collection_id=9',
        #'https://www.brooklynmuseum.org/opencollection/objects?offset=510&limit=30&object_year_begin=1850&on_view_only=1&collection_id=9',
        #'https://www.brooklynmuseum.org/opencollection/objects?offset=5400&limit=30&object_year_begin=1850&on_view_only=1&collection_id=9',
        #'https://www.brooklynmuseum.org/opencollection/objects?offset=570&limit=30&object_year_begin=1850&on_view_only=1&collection_id=9',
        #'https://www.brooklynmuseum.org/opencollection/objects?offset=600&limit=30&object_year_begin=1850&on_view_only=1&collection_id=9',
    ]


    def parse(self, response):
        # Eliminate the [2] from response.xpath to search all works on page
        #for href in response.xpath('//*[@id="works"]/div/div[2]/a/@href'):
        for href in response.xpath('/html/body/div[3]/div[5]/div/div[3]//a/@href'):    
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_artwork)

    def parse_artwork(self, response):
        if response.xpath('/html/body/div[3]/div[1]/div[2]/div[2]/h3/text()').extract()[0].strip() == "":
            artist = "Unknown"
            artist_sans_accents = "Unknown"
        else:
            artist = response.xpath('/html/body/div[3]/div[1]/div[2]/div[2]/h3/text()').extract()[0].strip()
            artist_sans_accents = remove_accents(artist)

        title = response.xpath('/html/body/div[3]/div[1]/div[2]/div[1]/h1/text()').extract()[0].strip()

        title_sans_accents = remove_accents(title)

        date = response.xpath('//strong[contains(text(), "DATES")]/parent::div[1]/text()').extract()[1].strip()

        medium = response.xpath('//strong[contains(text(), "MEDIUM")]/parent::div[1]/text()').extract()[1].strip()

        description = "None"

        dimensions = response.xpath('//strong[contains(text(), "DIMENSIONS")]/parent::div[1]/text()').extract()[1].strip()
        collection = "On View at the Brooklyn Museum"
        coordinates = "40.6716° N, 73.9627° W"
        address = "200 Eastern Pkwy, Brooklyn, NY 11238"
        pageurl = response.request.url

        accession_number = "BM" + response.xpath('//strong[contains(text(), "ACCESSION NUMBER")]/parent::div[1]/text()').extract()[1].strip()
        
        try:
            imageurl = response.xpath('/html/body/div[3]/div[1]/div[1]/div/div/div[1]/div/img/@src').extract()[0]
        except:
            imageurl = "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"
   
        timestamp = datetime.date.today().isoformat()
         
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