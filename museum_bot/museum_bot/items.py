# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy_djangoitem import DjangoItem
from app.models import Artwork #, Artist

#class ArtistItem(DjangoItem):
	#django_model = Artist

class ArtworkItem(DjangoItem):
	django_model = Artwork
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass