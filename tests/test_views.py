from contextlib import contextmanager

import pytest
from django.contrib.auth.signals import user_logged_in

from disguise.signals import disguise_applied, disguise_removed


@pytest.fixture(autouse=True)
def fix_settings(settings):
    settings.DISGUISE['can_disguise'] = ('example_project.stuff.'
                                         'test_can_disguise')


@pytest.fixture
def url():
    return '/'


@pytest.fixture
def mask_url():
    "A URL which put mask on a user"
    return '/disguise/'


@pytest.fixture
def unmask_url():
    "A URL that drops the mask from a user off"
    return '/disguise/remove/'


@contextmanager
def catch_signal(signal, handler):
    signal.connect(handler)
    yield handler
    signal.disconnect(handler)


@pytest.mark.parametrize(
    argnames='name, should',
    argvalues=[
        ('', False),
        ('regular_user', False),
        ('super_user', True),
    ],
    ids=[
        'an anonymous user can\'t',
        'a regular user can\'t',
        'a superuser can'
    ]
)
def test_if_user_can_see_disquise_form(
        client, url, name, should, request
):
    client.logout()
    if name:
        user = request.getfixturevalue(name)
        client.force_login(user=user)
    assert (b'<form ' in client.get(url).content) == should


def test_anonymous_access(client, regular_user, mask_url):
    client.logout()
    resp = client.post(mask_url, {'username': regular_user.username})
    assert resp.status_code == 403


def test_non_privileged_access(
        client, regular_user, super_user, mask_url
):
    client.force_login(regular_user)
    resp = client.post(mask_url, {'username': super_user.username})
    assert resp.status_code == 403


def test_mask_myself(client, mask_url, super_user, regular_user):
    client.force_login(super_user)
    resp = client.post(mask_url, {'username': regular_user.username},
                       follow=True)

    assert resp.status_code == 200
    assert resp.context['request'].user == regular_user
    assert resp.context['request'].original_user == super_user
    assert b'<form ' in resp.content

    # Disguise to superuser again
    resp = client.post(mask_url, {'username': super_user.username},
                       follow=True)
    assert resp.status_code == 200
    assert resp.context['request'].user == super_user
    assert resp.context['request'].original_user == super_user
    assert b'<form ' in resp.content


def test_unmask(client, unmask_url, super_user, regular_user):
    client.force_login(super_user)
    resp = client.get(unmask_url, follow=True)
    assert resp.context['request'].user == super_user


def test_disguise_by_username(client, super_user, regular_user, mask_url):
    client.force_login(super_user)
    resp = client.post(mask_url, {'username': regular_user.username},
                       follow=True)
    assert resp.context['request'].user == regular_user


def test_disguise_by_user_id(client, super_user, regular_user, mask_url):
    client.force_login(super_user)
    resp = client.post(mask_url, {'user_id': regular_user.id},
                       follow=True)
    assert resp.context['request'].user == regular_user


def test_signal_diguise_applied(client, super_user, regular_user, mask_url):
    client.force_login(super_user)

    def diguise_applied_handler(*args, **kwargs):
        assert kwargs['original_user'] == super_user
        assert kwargs['new_user'] == regular_user

    with catch_signal(disguise_applied, diguise_applied_handler):
        resp = client.post(mask_url, {'user_id': regular_user.id}, follow=True)
        assert resp.context['request'].user == regular_user


def test_signal_diguise_disapplied(client, super_user, regular_user, mask_url):
    client.force_login(super_user)

    def diguise_disapplied_handler(*args, **kwargs):
        assert kwargs['original_user'] == super_user

    with catch_signal(disguise_removed, diguise_disapplied_handler):
        resp = client.post(mask_url, {'user_id': regular_user.id}, follow=True)
        assert resp.context['request'].original_user == super_user


def test_user_logged_in_signal_does_not_fires_when_making_a_disguise(
        client, super_user, regular_user, mask_url, django_user_model
):
    def honeypot_handler(*args, **kwargs):
        "A handler crashes everything"
        raise RuntimeError('Gotcha!')

    # First, login as a superuser
    client.force_login(super_user)

    # Assuming, regular_user never logged in
    regular_user.last_login = None
    regular_user.save(update_fields=['last_login'])

    # Then add a signal that crashes everything!
    user_logged_in.connect(
        receiver=honeypot_handler,
        sender=django_user_model,
        dispatch_uid='break_all'
    )

    # Making a disguise
    resp = client.post(mask_url, {'user_id': regular_user.id}, follow=True)
    assert resp.context['request'].original_user == super_user

    # Oops, looks like nothing terrible happened ;)
    # Make sure, regular_user.last_login still None
    regular_user.refresh_from_db()
    assert regular_user.last_login is None


@pytest.mark.parametrize('field', ['user_id', 'username'])
def test_regression_cannot_swap_user_to_disabled_one(
    mask_url, client, super_user, regular_user, field
):
    client.force_login(super_user)

    regular_user.is_active = False
    regular_user.save(update_fields=['is_active'])

    resp = client.post(mask_url, {
        'user_id': {'user_id': regular_user.id},
        'username': {'username': regular_user.username}
    }[field], follow=True)

    assert not resp.context['form'].is_valid()
    assert field in resp.context['form'].errors


@pytest.mark.parametrize('field', ['user_id', 'username'])
def test_regression_cannot_swap_user_to_non_existing_one(
    mask_url, client, super_user, field
):
    client.force_login(super_user)

    resp = client.post(mask_url, {
        'user_id': {'user_id': 100500},
        'username': {'username': 'a-person-who-does-not-exist'}
    }[field], follow=True)

    assert not resp.context['form'].is_valid()
    assert field in resp.context['form'].errors
