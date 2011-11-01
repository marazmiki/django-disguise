from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.encoding import smart_unicode
from disguise.forms import DisguiseForm
import warnings

KEYNAME = 'django_disguise:original_user'
TAGNAME = '</body>'

def replace_insensitive(string, target, replacement):
    """ 
    Similar to string.replace() but is case insensitive
    Code borrowed from: http://forums.devshed.com/python-programming-11/case-insensitive-string-replace-490921.html
    """
    no_case = string.lower()
    index = no_case.rfind(target.lower())
    if index >= 0:
        return string[:index] + replacement + string[index + len(target):]
    else: # no results so return the original string
        return string


class DisguiseMiddleware(object):
    """
    Disguise user middleware
    """

    def test_disguise(self, request):
        if KEYNAME in request.session:
            return True

        if hasattr(request, 'original_user'):
            return True

        if request.user.has_perm('disguire.can_disguise'):
            return True

        return False

    def get_original_user(self, request):
        if KEYNAME in request.session:
            return request.session[KEYNAME]
        return request.user

    def process_request(self, request):
        """
        Runs during each request
        """
        if not hasattr(request, 'user'):
            warnings.warn("DisguiseMiddleware must be installed after "
                          "django.contrib.auth.middleware.AuthenticationMiddleware")
            return

        if not hasattr(request, 'session'):
            warnings.warn("DisguiseMiddleware must be installed after "
                          "django.contrib.sessions.middleware.SessionMiddleware")
            return

        if not request.user.is_authenticated():
            return

        if not self.test_disguise(request):
            return

        request.original_user = self.get_original_user(request)

    def process_response(self, request, response):
        """
        Runs during responding
        """
        if not request.user.is_authenticated():
            return response

        if not response.status_code == 200:
            return response

        if not response.get('content-type', '').startswith('text/html'):
            return response

        if self.test_disguise(request):
            # Render HTML code that helps to select disguise
            html = render_to_string('disguise/form.html', {
                'form': DisguiseForm(),
                'original_user' : getattr(request, 'original_user', None),
                'disguise_user' : getattr(request, 'user'),
            }, RequestContext(request))

            # Insert this code before </body>
            response.content = replace_insensitive(
                smart_unicode(response.content),    # Subject
                TAGNAME,                            # Search
                smart_unicode(html + TAGNAME)       # Replace
            )
        return response
