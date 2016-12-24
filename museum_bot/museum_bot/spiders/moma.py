import scrapy
import datetime
import json
import os

from museum_project.settings import BASE_DIR
from scrapy.spiders import Spider
from museum_bot.items import ArtworkItem
from app.tools import remove_accents
from app.models import Artwork

class MomaSpider(Spider):
    name = "moma"
    allowed_domains = ["moma.org"]
    start_urls = [
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=2&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=3&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=4&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=5&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=6&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=7&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=8&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=9&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=10&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=11&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=12&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=13&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=14&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=15&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=16&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=17&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=18&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=19&direction=fwd',
        'http://www.moma.org/collection/works?utf8=%E2%9C%93&q=&classifications=&on_view=1&page=20&direction=fwd',
    ]


    def parse(self, response):

        for href in response.xpath('//*[@id="works"]/div/div/a/@href'):    
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_artwork)

    def parse_artwork(self, response):
        artist = response.xpath('/html/body/div[3]/div/div/div[1]/div/div/h2/a/text()').extract()[0].strip()

        artist_sans_accents = remove_accents(artist)

        try:
            title = response.xpath('/html/body/div[3]/div/div/div[1]/div/div/h1/em/text()').extract()[0].strip()
        except:
            title = response.xpath('/html/body/div[3]/div/div/div[1]/div/div/h1/text()').extract()[0].strip()

        title_sans_accents = remove_accents(title)

        date = response.xpath('/html/body/div[3]/div/div/div[1]/div/div/h3/text()').extract()[0].strip()

        medium = response.xpath('/html/body/div[3]/div/div/div[1]/section[2]/div/div[1]/div[1]/dl/dt[contains(text(), "Medium")]/following-sibling::dd[1]/text()').extract()[0].strip()
 
        try:
            description = response.xpath('/html/body/div[3]/div[1]/section[2]/div/div[2]/div[1]/p[1]/text()').extract()[0].strip()
        except:
            description = "None"

        dimensions = response.xpath('/html/body/div[3]/div/div/div[1]/section[2]/div/div[1]/div[1]/dl/dd[2]/text()').extract()[0].strip()

        collection = "On View at MoMA"

        coordinates = "40.7607° N, 73.9762° W"

        address = "11 West 53rd Street, New York, NY 10019"

        pageurl = response.request.url

        accession_number = "MOMA" + response.xpath('/html/body/div[3]/div/div/div[1]/section[2]/div/div[1]/div[1]/dl/dt[contains(text(), "Object number")]/following-sibling::dd[1]/text()').extract()[0].strip()
        
        try:
            image = response.xpath('/html/body/div[3]/div/div/div[1]/section[1]/div/img/@srcset[1]').extract()[0].split(',')[0].strip('320w').strip()
            imagestripped = str(image)
            imageurl = 'http://www.moma.org'+imagestripped
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


        Artwork.objects.filter()

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