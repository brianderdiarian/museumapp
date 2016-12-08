from django.contrib import admin

# Register your models here.
#from django.contrib import admin
from app.models import Artwork

class ArtworkAdmin(admin.ModelAdmin):
	list_display = ('artist', 'title', 'collection', 'timestamp', 'sex')
#admin.site.register(Artist)
admin.site.register(Artwork, ArtworkAdmin)