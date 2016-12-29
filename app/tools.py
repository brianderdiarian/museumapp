import re
from datetime import date, timedelta
import unicodedata
from app.models import Artwork#, Artist
import collections



#strip parenthesis, double parenthesis, brackets, and double brackets from strings
def strip_parenthesis(test_str):
	ret = ''
	skip1c = 0
	skip2c = 0
	for i in test_str:
		if i == '[':
			skip1c += 1
		elif i == '(':
			skip2c += 1
		elif i == ']':
			skip1c -= 1
		elif i == ')':
			skip2c -= 1
		elif skip1c == 0 and skip2c == 0:
			ret += i
	return ret

#strip html tags
def cleanhtml(raw_html):
	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, '', raw_html)
	return cleantext

#show most recent results - yesterday to be safe that all indexes are complete
today = date.today()
yesterday = (date.today() - timedelta(1))


current = date.today()
#current = "2016-11-18"

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


#trying to make iterable list of movements
# movements = Artwork.objects.filter(timestamp=current).values_list("movements", flat=True)
# movements_list = list(movements)
# for i, s in enumerate(movements_list):
# 	movements_list[i] = s.split(',')

# final_list = sum(movements_list, [])
# allmovements = set(final_list)
# mlist = list(allmovements)
# for i, s in enumerate(mlist):
# 	mlist[i] = s.strip()

# mlist = list(filter(None, mlist))
# mlist = set(mlist)
# mlist = sorted(mlist)

#dict of artists and movements
#example: {'movements': 'Surrealism', 'artist': 'Salvador Dali'}, {'movements': 'Cubism', 'artist': 'Pablo Picasso'}
# am_dict = Artwork.objects.values("artist","movements")

# def movGenerator():
#  	for i in mlist:
#  		for x in am_dict:
#  			if i in x['movements']:
#  				yield (i, x['artist'])

# movGen = movGenerator()
# move=list(movGen)
# move=set(move)

# def ArtistMovement():
#  	for x in move:
#  		yield(dict({"Movement":x[0],"Artist":x[1]}))

# artist_movement = ArtistMovement()
# artist_movement = list(artist_movement)

# artist_by_movement = collections.defaultdict(list)
# for d in artist_movement:
#  	artist_by_movement[d['Movement']].append(d['Artist'])
# artist_by_movement = dict(artist_by_movement)

# #list of artists
# artistlist = Artwork.objects.filter(timestamp=current).values("artist").distinct().order_by('artist').exclude(artist__isnull=True).exclude(artist__exact='')