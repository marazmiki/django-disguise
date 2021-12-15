try:
    from django.urls import re_path as url
except ImportError:
    from django.conf.urls import url

from .views import Mask, MaskById, Unmask

urlpatterns = [
    url(r'^$', Mask.as_view(), name='disguise_mask'),
    url(r'^(?P<pk>\d+)/$', MaskById.as_view(), name='disguise_mask'),
    url(r'^remove/$', Unmask.as_view(), name='disguise_unmask'),
]
