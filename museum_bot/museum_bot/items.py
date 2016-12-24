# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy_djangoitem import DjangoItem
from app.models import Artwork, Artist, Display, Movement

class ArtworkItem(DjangoItem):
	django_model = Artwork
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass

class ArtistItem(DjangoItem):
	django_model = Artist

class DisplayItem(DjangoItem):
	django_model = Display

class MovementItem(DjangoItem):
	django_model = Movement