from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY

KEYNAME = 'django_disguise:original_user'
TAGNAME = 'body'
BACKEND = 'django.contrib.auth.backends.ModelBackend'

__all__ = ['KEYNAME', 'TAGNAME', 'SESSION_KEY', 'BACKEND_SESSION_KEY',
           'BACKEND']
