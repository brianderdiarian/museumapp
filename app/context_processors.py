from .models import Artwork, Movement, Artist, Collection, Display
from .tools import current, today#, mlist, artistlist, artist_by_movement
from django.db.models import Count

def movement_processor(request):
	movements = Movement.objects.filter(artist__artwork__display__end_date__gte=today).order_by('movement').values_list('movement', flat=True).distinct()

	#artists = Artist.objects.filter(artwork__display__end_date__gte=today).filter(artwork__display__start_date__lte=today).order_by('artist_sans_accents').distinct('artist_sans_accents').select_related()
	artists = Artist.objects.filter(artwork__display__end_date__gte=today).filter(artwork__display__start_date__lte=today).order_by('artist_sans_accents').values_list('artist_sans_accents', flat=True).distinct()

	#collections = Collection.objects.filter(display__start_date__lte=today).filter(display__end_date__gte=today).annotate(num_displays=Count('display')).order_by('-num_displays').distinct()
	collections = Collection.objects.filter(display__start_date__lte=today).filter(display__end_date__gte=today).annotate(num_displays=Count('display')).order_by('-num_displays').values_list('collection_name', flat=True).distinct()

	return {'movements': movements,
			'artists': artists,
			'collections': collections}
