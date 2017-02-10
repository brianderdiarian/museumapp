from .models import Artwork, Movement, Artist, Collection, Display
from .tools import current, today#, mlist, artistlist, artist_by_movement
from django.db.models import Count

def movement_processor(request):
	movements = Movement.objects.filter(artist__artwork__display__end_date__gte=today).order_by('movement').distinct()
	#movements = sorted(set(movements))

	artists = Artwork.objects.filter(display__end_date__gte=today).filter(display__start_date__lte=today).order_by('artist__artist_sans_accents').distinct('artist__artist_sans_accents')

	collections = Collection.objects.filter(display__start_date__lte=today).filter(display__end_date__gte=today).annotate(num_displays=Count('display')).order_by('-num_displays').distinct()


	return {'movements': movements,
			'artists': artists,
			'collections': collections,
			# 'artist_by_movement': artist_by_movement
			}
