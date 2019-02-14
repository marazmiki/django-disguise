from .const import KEYNAME

def can_disguise(request):
    return any((
        KEYNAME in request.session,
        hasattr(request, 'original_user'),
        request.user.has_perm('disguise.can_disguise')
    ))
