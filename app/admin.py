from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from app.models import Artwork, Artist, Collection, Display, NameVariant, Movement, Ethnicity, Nationality, Info, LastCrawl, Exhibition, UserProfile

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

class DisplayAdmin(admin.ModelAdmin):
    model = Display
    list_display = ('artwork', 'collection', 'start_date', 'end_date',)
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

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)