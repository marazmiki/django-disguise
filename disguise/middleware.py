from disguise.compat import get_user_model
from disguise.const import KEYNAME
from disguise.utils import can_disguise


class DisguiseMiddleware(object):
    """
    Disguise user middleware
    """

    def get_original_user(self, request):
        if KEYNAME in request.session:
            return get_user_model().objects.get(pk=request.session[KEYNAME])
        return request.user

    def process_request(self, request):
        """
        Injects the `original_user` attribute into HttpRequest object
        """
        if not request.user.is_authenticated():
            return
        if not can_disguise(request):
            return
        request.original_user = self.get_original_user(request)
