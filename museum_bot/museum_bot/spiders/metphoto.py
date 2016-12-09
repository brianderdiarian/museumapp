import scrapy
import datetime
import json
import os

from museum_project.settings import BASE_DIR
from scrapy.spiders import Spider
from museum_bot.items import ArtworkItem
from app.tools import strip_parenthesis
from app.tools import remove_accents
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
        # Eliminate the [2] from response.xpath to search all works on page
        #for href in response.xpath('//*[@id="works"]/div/div[2]/a/@href'):
        jsonresponse = json.loads(response.body_as_unicode())

        results = jsonresponse['results']

        for result in results:

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
                address = "1000 5th Ave, New York, NY 10028"
                coordinates = "40.7794° N, 73.9632° W"
            else:
                address = "945 Madison Ave, New York, NY 10021"
                coordinates = "40.7734° N, 73.9638° W"
            
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