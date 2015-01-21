# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django import test, get_version
from django.db.models.signals import post_save
from django.conf.urls import include, url
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission
from django.shortcuts import render
from disguise.compat import get_user_model
from disguise.forms import DisguiseForm
from disguise.signals import disguise_applied, disguise_disapplied
from disguise.utils import check_env


User = get_user_model()


class TestTemplateTag(test.TestCase):
    url = '/'

    def setUp(self):
        self.root = User.objects.create_superuser(username='root',
                                                  password='root',
                                                  email='root@example.com')
        self.user = User.objects.create_user(username='user',
                                             password='user',
                                             email='user@example.com')
        self.client = test.Client()
        self.client.login(username='root', password='root')

    def test_anonymous(self):
        self.client.logout()
        resp = self.client.get(self.url)
        self.assertNotContains(resp, '<form ')

    def test_regular_user(self):
        self.client.logout()
        self.client.login(username='user', password='user')
        resp = self.client.get(self.url)
        self.assertNotContains(resp, '<form ')

    def test_superuser(self):
        resp = self.client.get(self.url)
        self.assertContains(resp, '<form ')


class TestPermissions(test.TestCase):
    perm = Permission.objects.filter(codename='can_disguise')

    def test_post_save_permission(self):
        self.assertFalse(self.perm.exists())
        post_save.send(sender=Permission)
        self.perm.get()


class TestCheck(test.TestCase):
    def assertError(self, code):
        if get_version() >= '1.7':
            for er in check_env():
                if er.id == code:
                    return
            else:
                raise AssertionError('{} not happens'.format(code))
        else:
            self.assertRaises(ImproperlyConfigured, lambda: check_env())

    def test_all_correctly(self):
        self.assertFalse(bool(check_env()))

    def test_no_sessions_app(self):
        with self.settings(INSTALLED_APPS=[]):
            self.assertError('disguise.E001')

    def test_no_context_processors(self):
        with self.settings(TEMPLATE_CONTEXT_PROCESSORS=[]):
            self.assertError('disguise.E002')

    def test_no_sessions_middleware(self):
        with self.settings(MIDDLEWARE_CLASSES=[]):
            self.assertError('disguise.E003')

    def test_no_disguise_middleware(self):
        with self.settings(MIDDLEWARE_CLASSES=[]):
            self.assertError('disguise.E004')

    def test_middleware_order(self):
        MIDDLEWARE_CLASSES = [
            'disguise.middleware.DisguiseMiddleware'
            'django.contrib.sessions.middleware.SessionMiddeware'
        ]
        with self.settings(MIDDLEWARE_CLASSES=MIDDLEWARE_CLASSES):
            self.assertError('disguise.E005')


class TestForm(test.TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user', password='user',
                                        email='user@example.com')

    def test_form_invalid_everything(self):
        form = DisguiseForm({})
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

    def test_form_invalid_when_wrong_username(self):
        form = DisguiseForm({'username': self.user.username + '_not'})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_form_invalid_when_wrong_user_id(self):
        form = DisguiseForm({'user_id': 31337})
        self.assertFalse(form.is_valid())
        self.assertIn('user_id', form.errors)

    def test_form_valid_when_correct_username(self):
        form = DisguiseForm({'username': self.user.username})
        self.assertTrue(form.is_valid())

    def test_form_valid_when_correct_user_id(self):
        form = DisguiseForm({'user_id': self.user.pk})
        self.assertTrue(form.is_valid())


class DisguiseTest(test.TestCase):
    urls = 'disguise.tests'

    def setUp(self):
        self.mask_url = reverse('disguise_mask')
        self.unmask_url = reverse('disguise_unmask')
        self.root = User.objects.create_superuser(
            username='root',
            password='root',
            email='root@example.com'
        )
        self.user = User.objects.create_user(
            username='user',
            password='user',
            email='root@example.com'
        )
        self.client = test.Client()
        self.client.login(username='root', password='root')

    def mask_request(self, username=None, user_id=None, follow=False):
        data = {}
        if user_id:
            data.update(user_id=user_id)
        if username:
            data.update(username=username)
        return self.client.post(self.mask_url, data, follow=follow)

    def unmask_request(self, follow=False):
        return self.client.get(self.unmask_url, follow=follow)

    def test_anonymous_access(self):
        self.client.logout()
        resp = self.mask_request(username='user')
        self.assertEquals(302, resp.status_code)

    def test_non_privilegied_access(self):
        self.client.logout()
        self.client.login(username='user', password='user')
        resp = self.mask_request(username='root')
        self.assertEquals(302, resp.status_code)

    def test_mask_myself(self):
        """
        Tests if superuser can disguise to regular user by username
        """
        resp = self.mask_request(username='user', follow=True)
        self.assertEquals(200, resp.status_code)
        self.assertEquals(self.user, resp.context['request'].user)
        self.assertEquals(self.root, resp.context['request'].original_user)
        self.assertContains(resp, '<form ')

        # Disguise to superuser again
        resp = self.mask_request(username='root', follow=True)
        self.assertEquals(200, resp.status_code)
        self.assertEquals(self.root, resp.context['request'].original_user)
        self.assertEquals(self.root, resp.context['request'].user)
        self.assertContains(resp, '<form ')

    def test_unmask(self):
        self.mask_request(username='user', follow=True)
        resp = self.unmask_request(follow=True)
        self.assertEquals(self.root, resp.context['request'].user)

    def test_disguise_by_username(self):
        """
        Tests if superuser can disguise to regular user by username
        """
        resp = self.mask_request(username=self.user, follow=True)
        self.assertEquals(self.user, resp.context['request'].user)

    def test_disguise_by_user_id(self):
        """
        Tests if superuser can disguise to regular user by user id
        """
        resp = self.mask_request(user_id=self.user.pk, follow=True)
        self.assertEquals(self.user, resp.context['request'].user)

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


def index(request):
    return render(request, 'disguise/tests/index.html')


urlpatterns = [
    url(r'^disguise/', include('disguise.urls')),
    url(r'^accounts/login/$', index),
    url(r'^$', index),
]
