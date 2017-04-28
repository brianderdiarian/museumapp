"""defines URL patterns for app"""
import datetime
from django.conf.urls import url, include

from haystack.forms import SearchForm
from haystack.query import SearchQuerySet
from . import views
from haystack.views import SearchView, search_view_factory
from .tools import current, today, yesterday
from .forms import ArtSearchForm

sqs = SearchQuerySet().filter(start_date__lte=today).filter(end_date__gte=today)

urlpatterns = [

	url(r'^$', views.index, name='index'),
	url(r'^women/$', views.women, name='women'),
	url(r'^exhibitions/$', views.exhibitions, name='exhibitions'),
	url(r'^movement/(?P<movement_id>[0-9]+)/$', views.movement, name='movement'),
	url(r'^collection/(?P<collection_id>[0-9]+)/$', views.collection, name='collection'),
	url(r'^artist/(?P<artist_id>[0-9]+)/$', views.artist, name='artist'),
	url(r'^search/$', search_view_factory(
		view_class=SearchView, 
		form_class=ArtSearchForm,
		searchqueryset = sqs
	), name='haystack_search'),
	url(r'^about/$', views.about, name='about'),
	url(r'^contact/$', views.contact, name='contact'),
	url(r'^favartist/$', views.favArtist, name='favartist'),
	url(r'^profile/$', views.profile, name='profile'),
]