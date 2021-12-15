def my_own_can_disguise(request):
    return request.user.is_superuser or \
           getattr(request.user, 'last_name', '').lower() == 'bluth'


def test_can_disguise(request):
    from disguise.utils import can_disguise_default_behavior
    return can_disguise_default_behavior(request)


# should be!
__all__ = ['my_own_can_disguise', 'test_can_disguise']
