from django.contrib import admin

# Register your models here.
#from django.contrib import admin
from app.models import Artwork, Artist, Collection, Display, NameVariant, Movement, Ethnicity, Nationality

class ArtworkAdmin(admin.ModelAdmin):
	list_display = ('artist', 'title', 'collection', 'timestamp',)
	ordering = ('artist',)
admin.site.register(Artwork, ArtworkAdmin)

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
    list_display = ('get_artist', 'artwork', 'collection', 'start_date', 'end_date',)

    def get_artist(self, obj):
        return obj.artwork.artist
    get_artist.admin_order_field  = 'artwork'  #Allows column order sorting
    get_artist.short_description = 'Artist'  #Renames column head

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