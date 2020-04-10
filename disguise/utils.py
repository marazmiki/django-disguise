from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import Permission
from django.contrib.auth.signals import user_logged_in
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

from . import conf
from .const import BACKEND, BACKEND_SESSION_KEY, KEYNAME, SESSION_KEY
from .signals import disguise_applied, disguise_removed


def get_original_user(request):
    if KEYNAME in request.session:
        return get_user_model().objects.get(pk=request.session[KEYNAME])
    return request.user


def can_disguise(request):
    if KEYNAME in request.session:
        return True
    if getattr(request, 'original_user', False):
        return True
    if conf.CUSTOMIZED_CAN_DISGUISE:
        return conf.CUSTOMIZED_CAN_DISGUISE(request)
    else:
        return can_disguise_default_behavior(request)


def can_disguise_default_behavior(request):
    return request.user.has_perm('auth.can_disguise')


def swap_user(request, old_user, new_user):
    if KEYNAME not in request.session:
        request.original_user = old_user
        request.session[KEYNAME] = request.original_user.pk

    new_user.backend = BACKEND

    request.session[SESSION_KEY] = new_user.id
    request.session[BACKEND_SESSION_KEY] = new_user.backend

    receivers = user_logged_in.receivers
    user_logged_in.receivers = []
    login(request, new_user)
    user_logged_in.receivers = receivers

    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()

    if KEYNAME not in request.session:
        request.session[KEYNAME] = request.original_user.pk

    # If we change the user to the ``original_user`` we consider
    # just drop the mask off
    if new_user == request.original_user:
        disguise_removed.send(sender=get_user_model(),
                              original_user=request.original_user,
                              disguised_in_user=old_user,
                              request=request)
    else:
        disguise_applied.send(sender=get_user_model(),
                              original_user=request.original_user,
                              old_user=old_user,
                              new_user=new_user,
                              request=request)


def create_perms(*args, **kwargs):
    perms = (
        ('can_disguise', _('Can disguise')),
    )

    User = get_user_model()
    content_type = ContentType.objects.get_for_model(User)

    for codename, title in perms:
        Permission.objects.get_or_create(
            codename=codename,
            content_type=content_type,
            defaults={'name': title}
        )
