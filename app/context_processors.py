from .models import Artwork
from .tools import current, mlist, artistlist, artist_by_movement

def movement_processor(request):
	# movements = Artwork.objects.filter(timestamp=current).values_list("movements", flat=True)
	# movements_list = list(movements)
	# for i, s in enumerate(movements_list):
	# 	movements_list[i] = s.split(',')

	# final_list = sum(movements_list, [])
	# allmovements = set(final_list)
	# allmovements = list(allmovements)


	return {'mlist': mlist,
			'artistlist': artistlist,
			'artist_by_movement': artist_by_movement
			}
