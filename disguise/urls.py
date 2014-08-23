# coding: utf-8

from django.conf.urls import url
from disguise.views import mask, unmask


urlpatterns = [
    url('^$', mask, name='disguise_mask'),
    url('^unmask/$', unmask, name='disguise_unmask'),
]
