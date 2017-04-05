from django import forms

import haystack
from haystack.forms import SearchForm
from haystack.query import SearchQuerySet

class ArtSearchForm(SearchForm):

	def no_query_found(self):
		return self.searchqueryset.load_all()

class ContactForm(forms.Form):
	contact_name = forms.CharField(required=True)
	contact_email = forms.EmailField(required=True)
	content = forms.CharField(
		required=True,
		widget=forms.Textarea
	)

	def __init__(self, *args, **kwargs):
		super(ContactForm, self).__init__(*args, **kwargs)
		self.fields['contact_name'].label = "Your name:"
		self.fields['contact_email'].label = "Your email:"
		self.fields['content'].label = "What do you want to say?"