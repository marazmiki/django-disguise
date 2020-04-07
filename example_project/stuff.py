def my_own_can_disguise(request):
    print('!!!', request.user)
    return request.user.last_name.lower() == 'bluth'


def test_can_disguise(request):
    from disguise.utils import can_disguise_default_behavior
    return can_disguise_default_behavior(request)
