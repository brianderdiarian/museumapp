from django.utils import timezone
from haystack import indexes
from app.models import Display, Artwork

class DisplayIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    #title = indexes.CharField(model_attr='title')
    artwork = indexes.CharField(model_attr='artwork')
    collection = indexes.CharField(model_attr='collection')
    end_date = indexes.CharField(model_attr='end_date')
    start_date = indexes.CharField(model_attr='start_date')

    def get_model(self):
        return Display

    #def index_queryset(self, using=None):
    #    """Used when the entire index for model is updated."""
    #    return self.get_model().objects.all()