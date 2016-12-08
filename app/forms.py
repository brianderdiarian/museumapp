from django import forms
# from datetime import date, timedelta

import haystack
from haystack.forms import SearchForm
from haystack.query import SearchQuerySet

class ArtSearchForm(SearchForm):

	def no_query_found(self):
		return self.searchqueryset.load_all()