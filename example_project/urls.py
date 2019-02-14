from django.contrib import admin
from django.urls import include, path

from .views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('disguise/', include('disguise.urls')),
    path('', index),
]
