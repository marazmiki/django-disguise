# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.conf import settings
from disguise.const import KEYNAME
from disguise.compat import checks


def check_env():
    idx = settings.MIDDLEWARE_CLASSES.index

    # Checks if `django.contrib.sessions` application installed
    sessions_app_installed = ('django.contrib.sessions' in
                              settings.INSTALLED_APPS)

    # Checks if `django.core.context_processors.request` added
    # into TEMPLATE_CONTEXT_PROCESSORS tuple
    context_processors = ('django.core.context_processors.request' in
                          settings.TEMPLATE_CONTEXT_PROCESSORS)

    # Checks if sessions middleware is added into MIDDLEWARE_CLASSES
    sessions_middleware_installed = (
        'django.contrib.sessions.middleware.SessionMiddleware'
        in settings.MIDDLEWARE_CLASSES
    )

    # Checks if disguise middleware is added into MIDDLEWARE_CLASSES
    disguise_middleware_installed = ('disguise.middleware.DisguiseMiddleware'
                                     in settings.MIDDLEWARE_CLASSES)

    # Checks if sessions middleware installed before disguise one
    try:
        middleware_order = (
            idx('django.contrib.sessions.middleware.SessionMiddleware') <
            idx('disguise.middleware.DisguiseMiddleware')
        )
    except ValueError:
        middleware_order = False

    errors = []

    if not sessions_app_installed:
        errors.append(
            checks.Error(
                'Django sessions app is *not* installed',
                id='disguise.E001',
                hint=('Add the `django.contrib.sessions` into '
                      'your INSTALLED_APPS setting')
            )
        )
    if not context_processors:
        errors.append(
            checks.Error(
                'There is no `request` variable in template context',
                id='disguise.E002',
                hint=('Add the django.core.context_processors.request into '
                      'your TEMPLATE_CONTEXT_PROCESSORS setting')
            )
        )
    if not sessions_middleware_installed:
        errors.append(
            checks.Error(
                'Session middleware is *NOT* installed',
                id='disguise.E003',
                hint=('Add `django.contrib.sessions.middleware.Session'
                      'Middleware` into your MIDDLEWARE_CLASSES setting')
            )
        )
    if not disguise_middleware_installed:
        errors.append(
            checks.Error(
                'Disguise middleware is *NOT* installed',
                id='disguise.E004',
                hint=('Add `disguise.middleware.DisguiseMiddleware` '
                      'into your MIDDLEWARE_CLASSES setting')
            )
        )
    if not middleware_order:
        errors.append(
            checks.Error(
                'Session middleware must be installed before disguise one',
                id='disguise.E005',
                hint=('Swap the disguise.middleware.DisguiseMiddleware with '
                      'django.contrib.sessions.middleware.SessionMiddeware')
            )
        )

    return errors


def can_disguise(request):
    if KEYNAME in request.session:
        return True

    if hasattr(request, 'original_user'):
        return True

    if request.user.has_perm('disguise.can_disguise'):
        return True

    return False
