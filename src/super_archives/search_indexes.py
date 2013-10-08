# -*- coding: utf-8 -*-

from haystack import indexes

from .models import Message


class MessageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    mailinglist = indexes.CharField(model_attr='thread__mailinglist__name')
    description = indexes.CharField(model_attr='body')
    title = indexes.CharField(model_attr='subject_clean')
    modified = indexes.DateTimeField(model_attr='received_time')
    from_address_user_full_name = indexes.CharField(
        model_attr='from_address__user__get_full_name',
        null=True,
    )
    from_address_full_name = indexes.CharField(
        model_attr='from_address__get_full_name',
        null=True,
    )
    from_address_user_url = indexes.CharField(
        model_attr='from_address__user__get_absolute_url',
        null=True,
    )
    url = indexes.CharField(model_attr='url', null=True)

    def get_model(self):
        return Message

    def get_updated_field(self):
        return 'received_time'

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            thread__spam=False, spam=False
        ).exclude(thread__subject_token='')