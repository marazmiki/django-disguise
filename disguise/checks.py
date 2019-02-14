from django.conf import settings
from disguise.const import KEYNAME
from disguise.compat import checks


def check_env():
    middleware_list = settings.MIDDLEWARE
    context_processors = settings.TEMPLATES[0]['OPTIONS']['context_processors']  # _CONTEXT_PROCESSORS

    idx = middleware_list.index

    # Checks if `django.contrib.sessions` application installed
    sessions_app_installed = ('django.contrib.sessions' in
                              settings.INSTALLED_APPS)

    # Checks if `django.core.context_processors.request` added
    # into TEMPLATE_CONTEXT_PROCESSORS tuple
    cp_name = 'django.template.context_processors.request'
#    cp_name = 'django.core.context_processors.request'  # old way

    context_processors = (cp_name in
                          context_processors)

    # Checks if sessions middleware is added into MIDDLEWARE_CLASSES
    sessions_middleware_installed = (
        'django.contrib.sessions.middleware.SessionMiddleware'
        in middleware_list
    )

    # Checks if disguise middleware is added into MIDDLEWARE_CLASSES
    disguise_middleware_installed = ('disguise.middleware.DisguiseMiddleware'
                                     in middleware_list)

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
