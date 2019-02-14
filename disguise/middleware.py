from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin

from disguise.const import KEYNAME
from disguise.utils import can_disguise


class DisguiseMiddleware(MiddlewareMixin):
    def get_original_user(self, request):
        if KEYNAME in request.session:
            return get_user_model().objects.get(pk=request.session[KEYNAME])
        return request.user

    def process_request(self, request):
        """
        Injects the `original_user` attribute into HttpRequest object
        """
        if not request.user.is_authenticated:
            return
        if not can_disguise(request):
            return
        request.original_user = self.get_original_user(request)
