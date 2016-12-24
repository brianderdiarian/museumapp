from django.db import models
from django.contrib.postgres.fields import ArrayField

class Movement(models.Model):
	movement = models.CharField(max_length=255)

	def __str__(self):
		return self.movement

class Nationality(models.Model):
	nationality = models.CharField(max_length=255)

	def __str__(self):
		return self.nationality

class Ethnicity(models.Model):
	ethnicity = models.CharField(max_length=255)

	def __str__(self):
		return self.ethnicity

class Artist(models.Model):
	artist_sans_accents = models.CharField(max_length=255, blank=True)
	artist = models.CharField(max_length=255, blank=True)
	movements = models.CharField(max_length=255, blank=True)
	nationality = models.CharField(max_length=255)
	sex = models.CharField(max_length=255, blank=True)
	born = models.CharField(max_length=255, blank=True)
	died = models.CharField(max_length=255, blank=True)
	descriptors = models.CharField(max_length=255, blank=True)
	nationality = models.CharField(max_length=255, blank=True)
	new_nationality = models.ManyToManyField(Nationality, blank=True)
	ethnicity = models.ForeignKey(Ethnicity, null=True, blank=True)
	movement = models.ManyToManyField(Movement, blank=True)

	def get_movements(self):
		return ",".join([str(p) for p in self.movement.all()])

	def __str__(self):
		return self.artist_sans_accents

class Artwork(models.Model):
	artist = models.ForeignKey(Artist, null=True)
	#artist_sans_accents = models.CharField(max_length=255, blank=True)
	title = models.CharField(max_length=255, blank=True)
	title_sans_accents = models.CharField(max_length=255, blank=True)
	date = models.CharField(max_length=255, null=True, blank=True)
	medium = models.CharField(max_length=255)
	description = models.TextField(blank=True)
	dimensions = models.CharField(max_length=300)
	pageurl = models.CharField(max_length=255)
	accession_number = models.CharField(max_length=255, blank=True)
	imageurl = models.CharField(max_length=255)
	timestamp = models.DateField(auto_now=False, null=True)
	collection = models.CharField(max_length=255, blank=True)

	def __str__(self):
		return self.title

class Collection(models.Model):
	collection_name = models.CharField(max_length=255, blank=True)
	coordinates = models.CharField(max_length=255)
	address = models.CharField(max_length=255, null=True, blank=True)

	def __str__(self):
		return self.collection_name

class Display(models.Model):
	collection = models.ForeignKey(Collection, null=True)
	artwork = models.ForeignKey(Artwork, null=True)
	start_date = models.DateField(auto_now=False, null=True)
	end_date = models.DateField(auto_now=False, null=True)
	meta = models.TextField(blank=True)

	def __str__(self):
		return self.meta

class NameVariant(models.Model):
	name = models.CharField(max_length=255)
	artist = models.ForeignKey(Artist, null=True)

	def __str__(self):
		return self.name