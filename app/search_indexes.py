from django.utils import timezone
from haystack import indexes
from app.models import Display, Artwork
from app.tools import today

class DisplayIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    artwork = indexes.CharField(model_attr='artwork')
    collection = indexes.CharField(model_attr='collection')
    end_date = indexes.DateTimeField(model_attr='end_date')
    start_date = indexes.DateTimeField(model_attr='start_date')

    def get_model(self):
        return Display

    def index_queryset(self, using=None):
    # Used when the entire index for model is updated
    return self.get_model().objects.filter(start_date__lte=today).filter(end_date__gte=today)