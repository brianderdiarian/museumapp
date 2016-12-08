from django.utils import timezone
from haystack import indexes
from app.models import Artwork

class ArtworkIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    artist = indexes.CharField(model_attr='artist')
    artist_sans_accents = indexes.CharField(model_attr='artist_sans_accents')
    title = indexes.CharField(model_attr='title')
    title_sans_accents = indexes.CharField(model_attr='title_sans_accents')
    date = indexes.CharField(model_attr='date')
    medium = indexes.CharField(model_attr='medium')
    collection = indexes.CharField(model_attr='collection')
    #scrapedate = indexes.CharField(model_attr='scrapedate')
    timestamp = indexes.DateField(model_attr='timestamp')
    #imgurl = indexes.CharField(model_attr='imgurl')
    sex = indexes.CharField(model_attr='sex')
    nationality = indexes.CharField(model_attr='nationality')
    descriptors = indexes.CharField(model_attr='descriptors')
    movements = indexes.CharField(model_attr='movements')

    def get_model(self):
        return Artwork

    #def index_queryset(self, using=None):
    #    """Used when the entire index for model is updated."""
    #    return self.get_model().objects.all()