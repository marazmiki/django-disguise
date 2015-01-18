# coding: utf-8

from django.conf.urls import url
from disguise.views import MaskView, UnmaskView


urlpatterns = [
    url(r'^$', MaskView.as_view(), name='disguise_mask'),
    url(r'^unmask/$', UnmaskView.as_view(), name='disguise_unmask'),
]
