import scrapy
import datetime

from scrapy.spiders import Spider
from museum_bot.items import ArtworkItem

class WhitneySpider(Spider):
    name = "whitney"
    allowed_domains = ["collection.whitney.org"]
    start_urls = [
        'http://collection.whitney.org/group/5',
        #'http://collection.whitney.org/group/5?page=2',
        #'http://collection.whitney.org/group/5?page=3',
        #'http://collection.whitney.org/group/5?page=4',
        #'http://collection.whitney.org/group/5?page=5',
        #'http://collection.whitney.org/group/5?page=6',
    ]


    def parse(self, response):
        
        for href in response.xpath('//*[@id="main-webapp"]/div/ul/li[6]/div/div[1]/div/a/@href'):    
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_artwork)

    def parse_artwork(self, response):
         #artist = response.xpath('/html/body/div[3]/div[1]/div/div/h2/a[1]/text()').extract()[0]
         artist = response.xpath('//*[@id="main-webapp"]/div/div[4]/div[1]/div[2]/div/div[1]/div[1]/p[2]/text()').extract()[0]

         title = response.xpath('//*[@id="main-webapp"]/div/div[4]/div[1]/div[2]/div/div[1]/div[2]/p[2]/text()').extract()[0]
         date = response.xpath('//*[@id="main-webapp"]/div/div[4]/div[1]/div[2]/div/div[1]/div[3]/p[2]/text()').extract()[0]
         #find dd text where prior dt text is "medium" if error print "None"
         medium = response.xpath('//*[@id="main-webapp"]/div/div[4]/div[1]/div[2]/div/div[2]/div[1]/p[2]/text()').extract()[0]
         
         #try:
         #   description = response.xpath('/html/body/div[3]/div[1]/section[2]/div/div[2]/div[1]/p[1]/text()').extract()[0]
         #except:
         description = "None"
         #find dd text where prior dt text is "dimensions"
         dimensions = response.xpath('//*[@id="main-webapp"]/div/div[4]/div[1]/div[2]/div/div[2]/div[2]/p[2]/text()').extract()[0]
         collection = "Whitney Museum of American Art"
         coordinates = "40.7394° N, 74.0092° W"
         
         try:
            imageurl = response.xpath('//*[@id="main-webapp"]/div/div[4]/div[1]/div[1]/img/@src/text()').extract()
         except:
            imageurl = "http://www.novelupdates.com/img/noimagefound.jpg"   
         #imagestripped = str(image)
         #try:
         #   imageurl = 'http://www.moma.org'+imagestripped
         #except:
         #   imageurl = "None"
         
         timestamp = datetime.date.today().isoformat()

         address = "99 Gansevoort St, New York, NY 10014"
         
         return ArtworkItem(
            artist=artist,
            title=title,
            date=date,
            medium=medium,
            description=description,
            dimensions=dimensions,
            collection=collection,
            coordinates=coordinates,
            imageurl=imageurl,
            timestamp=timestamp,
            address=address,
        )


    #def parse_question(self, response):
    #    yield {
    #        'title': response.css('h1 a::text').extract_first(),
    #        'votes': response.css('.question .vote-count-post::text').extract_first(),
    #        'body': response.css('.question .post-text').extract_first(),
    #        'tags': response.css('.question .post-tag::text').extract(),
    #        'link': response.url,
    #    }