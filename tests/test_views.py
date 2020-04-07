from contextlib import contextmanager

import pytest

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


def test_non_privilegied_access(
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
        print('disguise DIZapplied', args, kwargs)
        # self.assertEquals(original_user, self.root)
        # self.assertEquals(old_user, self.user)

    with catch_signal(disguise_removed, diguise_disapplied_handler):
        resp = client.post(mask_url, {'user_id': regular_user.id}, follow=True)
        assert resp.context['request'].original_user == super_user
