from django.contrib import admin

# Register your models here.
#from django.contrib import admin
from app.models import Artwork, Artist, Collection, Display, NameVariant, Movement, Ethnicity, Nationality, Info, LastCrawl, Exhibition

class ArtworkAdmin(admin.ModelAdmin):
	list_display = ('artist', 'title', 'collection', 'timestamp',)
	ordering = ('artist',)
admin.site.register(Artwork, ArtworkAdmin)

class ExhibitionAdmin(admin.ModelAdmin):
    list_display = ('title', 'collection', 'timestamp',)
    ordering = ('title',)
admin.site.register(Exhibition, ExhibitionAdmin)

class ArtistAdmin(admin.ModelAdmin):
 	list_display = ('artist_sans_accents', 'artist', 'sex', 'movements', 'get_movements',)
admin.site.register(Artist, ArtistAdmin)

class CollectionAdmin(admin.ModelAdmin):
 	list_display = ('collection_name',)
admin.site.register(Collection, CollectionAdmin)

# class DisplayAdmin(admin.ModelAdmin):
#  	list_display = ('artwork', 'collection', 'start_date', 'end_date',)
# admin.site.register(Display, DisplayAdmin)

class DisplayAdmin(admin.ModelAdmin):
    model = Display
    list_display = ('artwork', 'collection', 'start_date', 'end_date',)

    #Filtering on side - for some reason, this works
    #list_filter = ['title', 'author__name']

admin.site.register(Display, DisplayAdmin)

class NameVarientAdmin(admin.ModelAdmin):
	list_display = ('name', 'artist')
admin.site.register(NameVariant, NameVarientAdmin)

class EthnicityAdmin(admin.ModelAdmin):
	list_display = ('ethnicity',)
admin.site.register(Ethnicity, EthnicityAdmin)

admin.site.register(Movement)

admin.site.register(Nationality)

class InfoAdmin(admin.ModelAdmin):
    list_display = ('about',)
admin.site.register(Info, InfoAdmin)

class LastCrawlAdmin(admin.ModelAdmin):
    list_display = ('spider_name',)
admin.site.register(LastCrawl, LastCrawlAdmin)