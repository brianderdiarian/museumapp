from django.db import models



# Create your models here.
class Artwork(models.Model):
	artist = models.CharField(max_length=255, blank=True)
	artist_sans_accents = models.CharField(max_length=255, blank=True)
	#artist_link = models.ForeignKey(Artist, null=True)
	title = models.CharField(max_length=255, blank=True)
	title_sans_accents = models.CharField(max_length=255, blank=True)
	date = models.CharField(max_length=255, blank=True)
	medium = models.CharField(max_length=255)
	description = models.TextField(blank=True)
	dimensions = models.CharField(max_length=255)
	collection = models.CharField(max_length=255)
	coordinates = models.CharField(max_length=255)
	pageurl = models.CharField(max_length=255)
	accession_number = models.CharField(max_length=255, blank=True)
	imageurl = models.CharField(max_length=255)
	#scrapedate = models.CharField(max_length=255)
	address = models.CharField(max_length=255, null=True, blank=True)
	timestamp = models.DateField(auto_now=False, null=True)
	sex = models.CharField(max_length=255, blank=True)
	born = models.CharField(max_length=255, blank=True)
	died = models.CharField(max_length=255, blank=True)
	movements = models.CharField(max_length=255, blank=True)
	descriptors = models.CharField(max_length=255, blank=True)
	nationality = models.CharField(max_length=255, blank=True)

	def __str__(self):
		#return self.artist
		return self.artist

#class Artist(models.Model):
	#name = models.CharField(max_length=255)
	#movement = models.CharField(max_length=255)
	#nationality = models.CharField(max_length=255)
	#gender = models.CharField(max_length=255, blank=True)
	#birthDate = models.CharField(max_length=255)
	#dateDeceased = models.CharField(max_length=255)
	#timestamp = models.DateTimeField(auto_now=True)

	#def __str__(self):
		#return self.artist
		#return self.name 