from django.contrib.auth import get_user_model
from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {
        'request': request,
        'users': get_user_model().objects.order_by('id')
    })
