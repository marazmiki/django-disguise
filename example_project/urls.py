from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, logout_then_login

from .views import index

try:
    from django.urls import include, re_path
except ImportError:
    from django.conf.urls import include, url as re_path

urlpatterns = [
    re_path(r'^disguise/', include('disguise.urls')),
    re_path(r'^$', index),
    re_path(r'^logout/$', logout_then_login, name='logout'),
    re_path(r'^login/$', LoginView.as_view(
        template_name='login.html',
        extra_context={
            'regular_users': get_user_model().objects.filter(
                is_superuser=False,
            )
        },
    ), name='login'),
]
