from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from .const import BACKEND, BACKEND_SESSION_KEY, KEYNAME, SESSION_KEY


def can_disguise(request):
    return any((
        KEYNAME in request.session,
        hasattr(request, 'original_user'),
        request.user.has_perm('disguise.can_disguise')
    ))


def swap_user(request, old_user, new_user):
    if KEYNAME not in request.session:
        request.original_user = old_user
        request.session[KEYNAME] = request.original_user.pk

    new_user.backend = BACKEND

    request.session[SESSION_KEY] = new_user.id
    request.session[BACKEND_SESSION_KEY] = new_user.backend

    login(request, new_user)

    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()

    if KEYNAME not in request.session:
        request.session[KEYNAME] = request.original_user.pk


def create_perms(sender, **kwargs):
    perms = (
        ('can_disguise', _('Can disguise')),
    )

    content_type = ContentType.objects.get_for_model(get_user_model())

    for codename, title in perms:
        Permission.objects.get_or_create(
            codename=codename,
            content_type=content_type,
            defaults={'name': title}
        )
