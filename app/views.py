import os

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, render_to_response
from haystack.query import SearchQuerySet
from haystack.generic_views import SearchView
from django.conf import settings
from django.http import HttpResponse
from django.db.models import Count, Q
from django.contrib.auth.models import User

from datetime import date, timedelta

from random import randint
from .models import Artwork, Display, Movement, Artist, Collection, Info, Nationality, Exhibition, FavoriteArtist
from .tools import current, yesterday, today

from .forms import ContactForm
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import Context
from django.template.loader import get_template

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')

def index(request):
    artworks = Artwork.objects.filter(display__end_date__gte=today).filter(display__start_date__lte=today).distinct().exclude(imageurl="https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg").order_by('-display__start_date')[:12]
    exhibitions = Exhibition.objects.filter(display__end_date__gte=today).filter(display__start_date__lte=today).order_by('display__start_date')[:4]
    
    user = request.user.id
    favoriteartists = FavoriteArtist.objects.filter(user=user).values_list('artist_id', flat=True)
    
    context={
    	'artworks': artworks,
    	'exhibitions': exhibitions,
    	'user': user,
    	'favoriteartists': favoriteartists,
    }
    return render(request, 'index.html', context)

def women(request):
	femaleArtists_list = Artwork.objects.filter(artist__sex="Female").filter(display__end_date__gte=today).filter(display__start_date__lte=today).distinct().prefetch_related().order_by('artist__artist_sans_accents')
	paginator = Paginator(femaleArtists_list, 24)

	user = request.user.id
	favoriteartists = FavoriteArtist.objects.filter(user=user).values_list('artist_id', flat=True)

	try:
		page = int(request.GET.get('page', '1'))
	except:
		page = 1

	try:
		femaleArtists = paginator.page(page)
	except(EmptyPage, InvalidPage):
		femaleArtists = paginator.page(paginator.num_pages)


	context = { 'femaleArtists': femaleArtists,
				'user': user,
				'favoriteartists': favoriteartists, }

	return render(request, 'women.html', context)

def movement(request, movement_id):
	displays = Display.objects.filter(Q(artwork__artist__movement=movement_id)| Q(exhibition__artist__movement=movement_id)).filter(end_date__gte=today).filter(start_date__lte=today).order_by('exhibition','artwork__artist').distinct()
	movement = Movement.objects.get(id=movement_id)
	paginator = Paginator(displays, 24)

	user = request.user.id
	favoriteartists = FavoriteArtist.objects.filter(user=user).values_list('artist_id', flat=True)

	try:
		page = int(request.GET.get('page', '1'))
	except:
		page = 1

	try:
		displays = paginator.page(page)
	except(EmptyPage, InvalidPage):
		displays = paginator.page(paginator.num_pages)

	context = { 'displays': displays,
				'movement': movement,
				'user': user,
				'favoriteartists': favoriteartists, }

	return render(request, 'movement.html', context)

def artist(request, artist_id):
	displays = Artwork.objects.filter(artist__id=artist_id).filter(display__end_date__gte=today).filter(display__start_date__lte=today).order_by('artist').distinct()
	artist = Artist.objects.get(id=artist_id)
	paginator = Paginator(displays, 24)

	user = request.user.id
	favoriteartists = FavoriteArtist.objects.filter(user=user).values_list('artist_id', flat=True)

	try:
		page = int(request.GET.get('page', '1'))
	except:
		page = 1

	try:
		displays = paginator.page(page)
	except(EmptyPage, InvalidPage):
		displays = paginator.page(paginator.num_pages)

	context = { 'displays': displays,
				'artist': artist, 
				'user': user,
				'favoriteartists': favoriteartists, }

	return render(request, 'artist.html', context)

def collection(request, collection_id):
	displays = Display.objects.filter(collection=collection_id).filter(end_date__gte=today).filter(start_date__lte=today).order_by('exhibition','artwork__artist').distinct()
	collection = Collection.objects.get(id=collection_id)
	paginator = Paginator(displays, 24)

	user = request.user.id
	favoriteartists = FavoriteArtist.objects.filter(user=user).values_list('artist_id', flat=True)

	try:
		page = int(request.GET.get('page', '1'))
	except:
		page = 1

	try:
		displays = paginator.page(page)
	except(EmptyPage, InvalidPage):
		displays = paginator.page(paginator.num_pages)

	movement_tally = Artwork.objects.filter(display__collection=collection).filter(display__end_date__gte=today).filter(display__start_date__lte=today).distinct().values('artist__movement__movement').annotate(Count('artist')).order_by('artist__movement__movement')

	male = Artwork.objects.filter(display__collection=collection).filter(artist__sex__contains="Male").filter(display__end_date__gte=today).filter(display__start_date__lte=today).distinct().count()
	female = Artwork.objects.filter(display__collection=collection).filter(artist__sex__contains="Female").filter(display__end_date__gte=today).filter(display__start_date__lte=today).distinct().count()
	unknown = Artwork.objects.filter(display__collection=collection).filter(artist__sex="").filter(display__end_date__gte=today).filter(display__start_date__lte=today).distinct().count()

	context = { 'displays': displays,
				'collection': collection,
				'movement_tally': movement_tally,
				'male': male,
				'female': female,
				'unknown': unknown,
				'user': user,
				'favoriteartists': favoriteartists,
				}

	return render(request, 'collection.html', context)

def about(request):
	infos = Info.objects.all()
	context = {'infos': infos}
	return render(request, 'about.html', context)

def contact(request):
	form_class = ContactForm

	# email logic
	if request.method == 'POST':
		form = form_class(data=request.POST)

		if form.is_valid():
			contact_name = request.POST.get('contact_name', '')
			contact_email = request.POST.get('contact_email', '')
			form_content = request.POST.get('content', '')

            # Email the profile with the 
            # contact information
			template = get_template('contact_template.txt')
			context = Context({
				'contact_name': contact_name,
				'contact_email': contact_email,
				'form_content': form_content,
				})
			content = template.render(context)

			email = EmailMessage(
				"New contact form submission",
				content,
				"artnewgo" +'',
				[EMAIL_ADDRESS],
				headers = {'Reply-To': contact_email }
            )

			email.send()
			return redirect('/')

	return render(request, 'contact.html', {'form': form_class, })
def exhibitions(request):
	displays = Exhibition.objects.filter(display__end_date__gte=today).filter(display__start_date__lte=today).distinct().order_by('display__start_date')
	paginator = Paginator(displays, 24)

	try:
		page = int(request.GET.get('page', '1'))
	except:
		page = 1

	try:
		displays = paginator.page(page)
	except(EmptyPage, InvalidPage):
		displays = paginator.page(paginator.num_pages)

	context = { 'displays': displays}

	return render(request, 'exhibitions.html', context)

def favArtist(request):
    if request.method == 'GET':
           artist_id = request.GET.get('artist_id')
           favartist = Artist.objects.get(pk=artist_id) #getting the liked posts
           userid = request.user.id
           current_user = User.objects.get(pk=userid)
           m = FavoriteArtist(artist=favartist, user=current_user) # Creating Like Object
           m.save()  # saving it to store in database
           return HttpResponse("Success!") # Sending an success response
    else:
           return HttpResponse("Request method is not a GET")


