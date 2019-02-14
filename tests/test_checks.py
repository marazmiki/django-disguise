import pytest

from disguise.checks import check_env

def check_fail(code):
    return any((error.id == code for error in check_env()))

def test_everything_is_good():
    assert not check_env()


def test_swear_if_no_contrib_sessions_app_installed(settings):
    settings.INSTALLED_APPS = ['disguise']
    assert check_fail('disguise.E001')


def test_swear_if_no_request_context_processor_installed(settings):
    settings.TEMPLATES[0]['OPTIONS']['context_processors'] = [
        'django.template.context_processors.debug',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]
    assert check_fail('disguise.E002')


def test_no_sessions_middleware(settings):
    settings.MIDDLEWARE = ['disguise.middleware.DisguiseMiddleware']
    assert check_fail('disguise.E003')


def test_no_disguise_middleware(settings):
    settings.MIDDLEWARE = [
        'django.contrib.sessions.middleware.SessionMiddeware'
    ]
    assert check_fail('disguise.E004')

def test_middleware_order_matter(settings):
    settings.MIDDLEWARE = [
        'disguise.middleware.DisguiseMiddleware'
        'django.contrib.sessions.middleware.SessionMiddeware'
    ]
    assert check_fail('disguise.E005')
