from .models import Artwork, Movement, Artist
from .tools import current, today#, mlist, artistlist, artist_by_movement

def movement_processor(request):
	movements = Movement.objects.filter(artist__artwork__display__end_date__gte=today).order_by('movement').distinct()
	#movements = sorted(set(movements))

	artists = Artist.objects.filter(artwork__display__end_date__gte=today).exclude(artist_sans_accents__contains="Attributed").order_by('artist_sans_accents').distinct()


	return {'movements': movements,
			'artists': artists,
			# 'artist_by_movement': artist_by_movement
			}
