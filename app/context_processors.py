from .models import Artwork, Movement, Artist, Collection, Display
from .tools import current, today
from django.db.models import Count

def movement_processor(request):
	movements = Movement.objects.only('movement', 'id').filter(artist__artwork__display__end_date__gte=today).distinct().order_by('movement').values('movement','id')

	artists = Artist.objects.only('artist_sans_accents','id').distinct().filter(artwork__display__end_date__gte=today).filter(artwork__display__start_date__lte=today).order_by('artist_sans_accents').values('artist_sans_accents','id')

	collections = Collection.objects.only('collection_name','id').distinct().order_by('collection_name').values('collection_name','id')

	return {
		'movements': movements,
		'artists': artists,
		'collections': collections,
	}
