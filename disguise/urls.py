from django.conf.urls import url, patterns
from disguise.views import mask, unmask


urlpatterns = patterns('disguise.views',
    url('^$', 'mask', name='disguise_mask'),
    url('^unmask/$', 'unmask', name='disguise_unmask'),
)

