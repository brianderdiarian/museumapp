from .models import Artwork, Movement, Artist, Collection, Display
from .tools import current, today
from django.db.models import Count

def movement_processor(request):
	movements = Movement.objects.only('movement', 'id').filter(artist__artwork__display__end_date__gte=today).distinct().order_by('movement').values('movement','id').select_related()

	artists = Artist.objects.only('artist_sans_accents','id').distinct().filter(artwork__display__end_date__gte=today).filter(artwork__display__start_date__lte=today).order_by('artist_sans_accents').values('artist_sans_accents','id').select_related()

	collections = Collection.objects.only('collection_name','id').distinct().filter(display__start_date__lte=today).filter(display__end_date__gte=today).annotate(num_displays=Count('display')).order_by('-num_displays').values('collection_name','id').select_related()

	return {
		'movements': movements,
		'artists': artists,
		'collections': collections,
	}
