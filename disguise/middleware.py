from django.utils.deprecation import MiddlewareMixin

from .utils import can_disguise, get_original_user


class DisguiseMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """
        Adds an `original_user`` attribute to the HttpRequest instance
        to make it available in the swap
        """
        if not request.user.is_authenticated:
            return
        if not can_disguise(request):
            return
        request.original_user = get_original_user(request)
