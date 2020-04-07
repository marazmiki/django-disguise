from django.conf import settings
from django.core import checks
from django.utils.module_loading import import_string

SESSIONS_APP = 'django.contrib.sessions'
SESSIONS_MIDDLEWARE = 'django.contrib.sessions.middleware.SessionMiddleware'
DISGUISE_MIDDLEWARE = 'disguise.middleware.DisguiseMiddleware'
REQUEST_CONTEXT_PROCESSOR = 'django.template.context_processors.request'


class DisguiseTag(checks.Tags):
    pass


def sessions_app_installed():
    return SESSIONS_APP in settings.INSTALLED_APPS


def sessions_middleware_installed():
    return SESSIONS_MIDDLEWARE in settings.MIDDLEWARE


def disguise_middlware_installed():
    return DISGUISE_MIDDLEWARE in settings.MIDDLEWARE


def request_context_processor_installed():
    return any((
        REQUEST_CONTEXT_PROCESSOR
        in t.get('OPTIONS', {}).get('context_processors')
        for t in settings.TEMPLATES
    ))


def middleware_right_order():
    idx = settings.MIDDLEWARE.index
    try:
        return idx(SESSIONS_MIDDLEWARE) < idx(DISGUISE_MIDDLEWARE)
    except ValueError:
        return False


def disguise_settings():
    if not hasattr(settings, 'DISGUISE'):
        return True
    if not isinstance(settings.DISGUISE, dict):
        return False
    return True


def custom_can_disguise():
    custom_func = getattr(settings, 'DISGUISE', {}).get('can_disguise')
    if custom_func is None:
        return True
    try:
        import_string(custom_func)
        return True
    except ImportError:
        return False


def check_env(*args, **kwargs):
    errors = []

    if not sessions_app_installed():
        errors.append(
            checks.Error(
                'The "django.contrib.sessions" application isn\'t installed',
                id='disguise.E001',
                hint=('Add the `django.contrib.sessions` into '
                      'your INSTALLED_APPS setting')
            )
        )
    if not request_context_processor_installed():
        errors.append(
            checks.Error(
                'There is no "request" variable in template context',
                id='disguise.E002',
                hint=(
                    'Add the {0} into your TEMPLATE_CONTEXT_PROCESSORS '
                    'setting'.format(REQUEST_CONTEXT_PROCESSOR)
                )
            )
        )
    if not sessions_middleware_installed():
        errors.append(
            checks.Error(
                'Session middleware is *NOT* installed',
                id='disguise.E003',
                hint=('Add `django.contrib.sessions.middleware.Session'
                      'Middleware` into your MIDDLEWARE_CLASSES setting')
            )
        )
    if not disguise_middlware_installed():
        errors.append(
            checks.Error(
                'Disguise middleware is *NOT* installed',
                id='disguise.E004',
                hint=('Add `disguise.middleware.DisguiseMiddleware` '
                      'into your MIDDLEWARE_CLASSES setting')
            )
        )
    if not middleware_right_order():
        errors.append(
            checks.Error(
                'Session middleware must be installed before disguise one',
                id='disguise.E005',
                hint=('Swap the disguise.middleware.DisguiseMiddleware with '
                      'django.contrib.sessions.middleware.SessionMiddeware')
            )
        )
    if not disguise_settings():
        errors.append(
            checks.Error(
                'The DISGUISE settings could be only a dict',
                id='disguise.E006',
                hint=(
                    'Please the full path to the function you want to use to '
                    'and make sure it is a callable object.'
                )
            )
        )

    if not custom_can_disguise():
        errors.append(
            checks.Error(
                'Custom `can_disguise` you specified is not a callable object',
                id='disguise.E007',
                hint=(
                    'Please the full path to the function you want to use to '
                    'and make sure it is a callable object.'
                )
            )
        )

    return errors
