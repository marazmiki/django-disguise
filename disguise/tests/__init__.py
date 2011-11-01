from django import test
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from disguise import urls

class EnvironmentTest(test.TestCase):
    def test_request_context_processors(self):
        """
        Tests that request context processor is enabled
        """
        assert 'django.core.context_processors.request' in \
        settings.TEMPLATE_CONTEXT_PROCESSORS

    def test_session_app_enabled(self):
        """
        Tests that django session application is installed
        """
        assert 'django.contrib.sessions' in settings.INSTALLED_APPS

    def test_middleware_session_enabled(self):
        """
        Tests that django session middleware is enabled
        """
        assert 'django.contrib.sessions.middleware.SessionMiddleware' in \
        settings.MIDDLEWARE_CLASSES

    def test_middleware_disguise_enabled(self):
        """
        Tests that disguise middleware is enabled
        """
        assert 'disguise.middleware.DisguiseMiddleware' in \
        settings.MIDDLEWARE_CLASSES

    def test_middleware_disguiseorder(self):
        """
        Tests that disguise middleware follows after session middleware
        """
        idx = settings.MIDDLEWARE_CLASSES.index

        assert idx('django.contrib.sessions.middleware.SessionMiddleware') < \
               idx('disguise.middleware.DisguiseMiddleware')  

class DisguiseTest(test.TestCase):
    urls = 'disguise.tests.urls'
    
    def patch_urls(self):
        urls.urlpatterns += urls.patterns('',
            (r'^$', lambda request: render(request, 'disguise/tests/index.html')),
        )

    def setUp(self):
        self.patch_urls()
        self.john = User.objects.create_superuser(username='john',
                                                  password='smith',
                                                  email='john@smith.com')
        self.jane = User.objects.create_user(username='jane',
                                             password='smith',
                                             email='jane@smith.com')
        self.client = test.Client()
        self.url_mask = reverse('disguise_mask')
        self.url_unmask = reverse('disguise_unmask')

    def test_mask_myself(self):
        """
        Tests if superuser can disguise to regular user by username
        """
        # Login as superuser
        self.client.login(username='john', password='smith')

        # Disguise to regular user
        resp = self.client.post(self.url_mask, data={'username': 'jane'}, follow=True)
        self.assertEquals(self.jane, resp.context['request'].user)
        self.assertEquals(self.john, resp.context['request'].original_user )

        # Disguise to superuser again
        resp = self.client.post(self.url_mask, data={'username': 'john'}, follow=True)
        self.assertEquals(self.john, resp.context['request'].original_user)
        self.assertEquals(self.john, resp.context['request'].user)

    def test_unmask(self):
        """
        Tests if superuser can disguise to regular user by username
        """
        self.client.login(username='john', password='smith')
        resp = self.client.post(self.url_mask, data={'username': 'jane'}, follow=True)
        resp = self.client.get(self.url_unmask, follow=True)
        self.assertEquals(self.john, resp.context['request'].user)

    def test_by_username(self):
        """
        Tests if superuser can disguise to regular user by username
        """
        self.client.login(username='john', password='smith')
        resp = self.client.post(self.url_mask, data={'username': 'jane'}, follow=True)
        self.assertEquals(self.jane, resp.context['request'].user)

    def test_by_user_id(self):
        """
        Tests if superuser can disguise to regular user by user id
        """
        self.client.login(username='john', password='smith')
        resp = self.client.post(self.url_mask, data={'user_id': '2'}, follow=True)
        self.assertEquals(self.jane, resp.context['request'].user)

    def test_update_last_login(self):
        """
        Tests that last login time for user is changed
        """
        self.client.login(username='john', password='smith')
        was = self.jane.last_login
        resp = self.client.post(self.url_mask, data={'user_id': '2', 'update_last_login':'1'}, follow=True)
        self.assertNotEquals(was, resp.context['request'].user.last_login)

    def test_not_update_last_login(self):
        """
        Tests that last login time for user isn't changed
        """
        self.client.login(username='john', password='smith')
        was = self.jane.last_login
        resp = self.client.post(self.url_mask, data={'user_id': '2'}, follow=True)
        self.assertTrue(was < resp.context['request'].user.last_login)
    
    def test_permission_required(self):
        """
        Tests that regular user can't disguise
        """
        self.client.login(username='jane', password='smith')
        resp = self.client.post(self.url_mask, data={'username': 'john'}, follow=True)
        self.assertEquals(self.jane, resp.context['request'].user)
