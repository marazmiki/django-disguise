from django.contrib import admin

from .views import index

try:
    from django.urls import include, re_path
except ImportError:
    from django.conf.urls import include, url as re_path

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^disguise/', include('disguise.urls')),
    re_path(r'^$', index),
]
