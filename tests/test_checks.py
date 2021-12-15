import pytest

from disguise.checks import check_env


def error_happened(code):
    return any((error.id == code for error in check_env()))


def error_did_not_happen(code):
    return not error_happened(code)


def test_everything_is_good():
    assert not check_env()


def test_e001_swear_if_no_contrib_sessions_app_installed(settings):
    settings.INSTALLED_APPS = ['django.contrib.auth', 'disguise']
    assert error_happened('disguise.E001')


def test_e002_swear_if_no_request_context_processor_installed(settings):
    settings.TEMPLATES[0]['OPTIONS']['context_processors'] = [
        'django.template.context_processors.debug',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]
    assert error_happened('disguise.E002')


def test_e003_no_sessions_middleware(settings):
    settings.MIDDLEWARE = ['disguise.middleware.DisguiseMiddleware']
    assert error_happened('disguise.E003')


def test_e004_no_disguise_middleware(settings):
    settings.MIDDLEWARE = [
        'django.contrib.sessions.middleware.SessionMiddeware'
    ]
    assert error_happened('disguise.E004')


def test_e005_middleware_order_matter(settings):
    settings.MIDDLEWARE = [
        'disguise.middleware.DisguiseMiddleware'
        'django.contrib.sessions.middleware.SessionMiddeware'
    ]
    assert error_happened('disguise.E005')


@pytest.mark.parametrize(
    argnames='value, expect_error',
    argvalues=[
        ({}, False),
        ('', True),
        (b'', True),
        ([], True),
        (None, True),
        (set(), True),
    ],
    ids=[
        'dict', 'string', 'bytes', 'list', 'none', 'set'
    ]
)
def test_e006_disguise_config_dict(settings, value, expect_error):
    settings.DISGUISE = value
    if expect_error:
        assert error_happened('disguise.E006')
    else:
        assert error_did_not_happen('disguise.E006')


@pytest.mark.parametrize(
    argnames='can_disguise, fail_expected',
    argvalues=[
        (None, False),
        ('example_project.stuff.my_own_can_disguise', False),
        ('example_project.stuff.__all__', True),
        ('does.not.exist', True),
    ],
    ids=[
        'no custom can_disguise set',
        'a_valid_callable',
        'a_valid_non_callable',
        'invalid'
    ])
def test_e007_customized_can_disguise(settings, can_disguise, fail_expected):
    settings.DISGUISE = {
        'can_disguise': can_disguise
    }
    if fail_expected:
        assert error_happened('disguise.E007')
    else:
        assert error_did_not_happen('disguise.E007')


@pytest.mark.parametrize(
    argnames='widget_form, fail_expected',
    argvalues=[
        (None, False),
        ('disguise.forms.DisguiseForm', False),
        ('not.exist', True),
        ('example_project.stuff.can_disguise', True),
        ('example_project.stuff.WrongWidgetForm', True),
    ],
    ids=[
        'not set',
        'right widget form (i.e. a form with get_user() method)',
        'non existing way',
        'not a django form',
        'invalid widget form (a form w/o get_user() method)',
    ]
)
def test_e008_customized_widget_form(settings, widget_form, fail_expected):
    settings.DISGUISE = {
        'widget_form': widget_form,
    }
    if fail_expected:
        assert error_happened('disguise.E008')
    else:
        assert error_did_not_happen('disguise.E008')
