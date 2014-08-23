# coding: utf-8

from django.conf.urls import include, url, patterns    # NOQA
from django.http import HttpResponse
from django.template import Context, Template


def index(request):
    template = Template("")
    context = Context({'request': request, 'user': request.user})
    return HttpResponse(template.render(context))


urlpatterns = [
    url('^disguise/', include('disguise.urls')),
    url('^accounts/login/$', index),
    url('^$', index),
]
