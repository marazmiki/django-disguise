# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls.defaults import *
from django.http import HttpResponse
from django.template import Context, Template

def index(request):
    template = Template("")
    context = Context({'request': request, 'user': request.user})
    return HttpResponse( template.render(context) )

urlpatterns = patterns('',
    url('^disguise/', include('disguise.urls')),
    url('^accounts/login/$',     index),
    url('^$',                    index),
)
