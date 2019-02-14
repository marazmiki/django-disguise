try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User

    def get_user_model():
        return User


try:
    from django.core import checks
    assert hasattr(checks, 'Error')
except (ImportError, AssertionError):
    from django.core.exceptions import ImproperlyConfigured

    class Checks(object):
        class Error(object):
            def __init__(self, message, hint='', error='', id=''):
                raise ImproperlyConfigured(message, id)
    checks = Checks()
