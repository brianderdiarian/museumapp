import os

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, render_to_response
from haystack.query import SearchQuerySet
from haystack.generic_views import SearchView
from django.conf import settings
from django.http import HttpResponse

from datetime import date, timedelta

from random import randint
from .models import Artwork, Display, Movement, Artist, Collection, Info
from .tools import current, yesterday, today#, mlist, artist_by_movement

from .forms import ContactForm
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import Context
from django.template.loader import get_template

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')

# yester = current - timedelta(1)

def index(request):
    #artists = Artwork.objects.filter(timestamp__gte=current).order_by('?')[:12]
    displays = Display.objects.filter(end_date__gte=today).order_by('?')[:12]
    context={'displays': displays}
    return render(request, 'index.html', context)

# def new(request):
# 	old = Artwork.objects.filter(timestamp=yester).values_list('accession_number', flat=True)
# 	new = Artwork.objects.filter(timestamp=current)

# 	context = { 'old': yesterday,
# 				'today': today }
# 	return render(request, 'new.html', context)

def women(request):
	femaleArtists_list = Artwork.objects.filter(artist__sex="Female").filter(display__end_date__gte=today).order_by('?')

	paginator = Paginator(femaleArtists_list, 24)

	try:
		page = int(request.GET.get('page', '1'))
	except:
		page = 1

	try:
		femaleArtists = paginator.page(page)
	except(EmptyPage, InvalidPage):
		femaleArtists = paginator.page(paginator.num_pages)


	context = { 'femaleArtists': femaleArtists}

	return render(request, 'women.html', context)

def movement(request, movement_id):
	artworks = Artwork.objects.filter(artist__movement__id=movement_id).filter(display__end_date__gte=today).order_by('artist__artist_sans_accents')
	movement = Movement.objects.get(id=movement_id)
	paginator = Paginator(artworks, 24)

	try:
		page = int(request.GET.get('page', '1'))
	except:
		page = 1

	try:
		artworks = paginator.page(page)
	except(EmptyPage, InvalidPage):
		artworks = paginator.page(paginator.num_pages)

	context = { 'artworks': artworks,
				'movement': movement, }

	return render(request, 'movement.html', context)

def artist(request, artist_id):
	artworks = Artwork.objects.filter(artist__id=artist_id).filter(display__end_date__gte=today)
	artist = Artist.objects.get(id=artist_id)
	paginator = Paginator(artworks, 24)

	try:
		page = int(request.GET.get('page', '1'))
	except:
		page = 1

	try:
		artworks = paginator.page(page)
	except(EmptyPage, InvalidPage):
		artworks = paginator.page(paginator.num_pages)

	context = { 'artworks': artworks,
				'artist': artist, }

	return render(request, 'artist.html', context)

def collection(request, collection_id):
	artworks = Artwork.objects.filter(display__collection__id=collection_id).filter(display__end_date__gte=today).order_by('artist__artist_sans_accents')
	collection = Collection.objects.get(id=collection_id)
	paginator = Paginator(artworks, 24)

	try:
		page = int(request.GET.get('page', '1'))
	except:
		page = 1

	try:
		artworks = paginator.page(page)
	except(EmptyPage, InvalidPage):
		artworks = paginator.page(paginator.num_pages)

	context = { 'artworks': artworks,
				'collection': collection, }

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


