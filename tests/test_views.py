import pytest

from disguise.signals import disguise_applied, disguise_disapplied


@pytest.fixture
def url():
    return '/'


@pytest.fixture
def mask_url():
    return '/disguise/'

@pytest.fixture
def unmask_url():
    return '/disguise/unmask/'



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
    assert resp.status_code == 302

def test_non_privilegied_access(
        client, regular_user, super_user, mask_url
    ):
    client.force_login(regular_user)
    resp = client.post(mask_url, {'username': super_user.username})
    assert resp.status_code == 302

def test_mask_myself(client, mask_url, super_user, regular_user):
    client.force_login(super_user)
    resp = client.post(mask_url, {'username': regular_user.username}, follow=True)

    assert resp.status_code == 200
    assert resp.context['request'].user == regular_user
    assert resp.context['request'].original_user == super_user
    assert b'<form ' in resp.content

    # Disguise to superuser again
    resp = client.post(mask_url, {'username': super_user.username}, follow=True)
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
    resp = client.post(mask_url, {'username': regular_user.username}, follow=True)
    assert resp.context['request'].user == regular_user

def test_disguise_by_user_id(client, super_user, regular_user, mask_url):
    client.force_login(super_user)
    resp = client.post(mask_url, {'user_id': regular_user.id}, follow=True)
    assert resp.context['request'].user == regular_user


"""    
    def test_disguise_applied_signal(self):
        self._entered = False

        def handler(**kwargs):
            original_user = kwargs['original_user']
            new_user = kwargs['new_user']

            self.assertEquals(original_user, self.root)
            self.assertEquals(new_user, self.user)
            self._entered = True

        disguise_applied.connect(handler, sender=User, dispatch_uid='test')

        self.mask_request(username=self.user, follow=True)
        self.assertTrue(self._entered)

        disguise_applied.disconnect(handler, sender=User, dispatch_uid='test')
        del self._entered

    def test_disguise_disapplied_signal(self):
        self._entered = False

        def handler(**kwargs):
            original_user = kwargs['original_user']
            old_user = kwargs['old_user']

            self.assertEquals(original_user, self.root)
            self.assertEquals(old_user, self.user)
            self._entered = True

        disguise_disapplied.connect(handler, sender=User,
                                    dispatch_uid='test')
        self.mask_request(username=self.user, follow=True)
        self.unmask_request(follow=True)
        self.assertTrue(self._entered)
        disguise_disapplied.disconnect(handler, sender=User,
                                       dispatch_uid='test')
        del self._entered
        """
