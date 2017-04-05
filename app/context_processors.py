from .models import Artwork, Movement, Artist, Collection, Display
from .tools import current, today
from django.db.models import Count

def movement_processor(request):
	movements = Movement.objects.filter(artist__artwork__display__end_date__gte=today).order_by('movement').values('movement','id').distinct()

	artists = Artist.objects.filter(artwork__display__end_date__gte=today).filter(artwork__display__start_date__lte=today).order_by('artist_sans_accents').values('artist_sans_accents','id').distinct()

	collections = Collection.objects.filter(display__start_date__lte=today).filter(display__end_date__gte=today).annotate(num_displays=Count('display')).order_by('-num_displays').values('collection_name','id').distinct()

	return {
		'movements': movements,
		'artists': artists,
		'collections': collections,
	}
