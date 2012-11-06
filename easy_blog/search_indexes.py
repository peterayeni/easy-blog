#-*- coding: utf-8 -*-

from haystack import indexes
from easy_blog.models import Story


class StoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='author')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Story

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.published()
