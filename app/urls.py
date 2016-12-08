"""defines URL patterns for app"""
import datetime
from django.conf.urls import url, include

from haystack.forms import SearchForm
from haystack.query import SearchQuerySet
from . import views
from haystack.views import SearchView, search_view_factory
from .tools import current
from .forms import ArtSearchForm

sqs = SearchQuerySet().filter(timestamp__gte=current)

urlpatterns = [
	#homepage
	url(r'^$', views.index, name='index'),

	url(r'^new/$', views.new, name='new'),

	url(r'^women/$', views.women, name='women'),

	url(r'^test/$', views.test, name='test'),
	
	url(r'^search/$', search_view_factory(
		view_class=SearchView, 
		form_class=ArtSearchForm,
		searchqueryset = sqs
	), name='haystack_search'),
]