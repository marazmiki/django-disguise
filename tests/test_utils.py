import pytest
from django.contrib.auth.models import Permission
from django.contrib.sessions.middleware import SessionMiddleware

from disguise.utils import can_disguise, create_perms
from example_project.stuff import my_own_can_disguise


@pytest.mark.parametrize(
    argnames='user_type, expected',
    argvalues=[
        ('superuser', True),
        ('regular_user', False),
        ('staff_user', False),
        ('staff_user_with_perm', True),
    ]
)
def test_can_disguise_default_behavior(
        rf, django_user_model,
        regular_user, super_user,
        expected, user_type
):
    user = regular_user

    if user_type == 'superuser':
        user = super_user
    elif user_type == 'staff_user':
        user.is_staff = True
        user.save()
    elif user_type == 'staff_user_with_perm':
        create_perms()
        user.is_staff = True
        user.user_permissions.add(
            Permission.objects.get(codename='can_disguise')
        )
        user.save()

    request = rf.get('/')
    request.user = user
    SessionMiddleware().process_request(request)
    request.session.save()

    assert can_disguise(request) is expected


@pytest.mark.parametrize('last_name, can', [
    ('Bluth', True),
    ('bluth', True),
    ('blUth', True),
    ('Reynolds', False),
    ('', False)
])
def test_can_disguise_custom_behavior(rf, regular_user,
                                      last_name, can, monkeypatch):
    from disguise import utils

    monkeypatch.setattr(utils.conf, 'CUSTOMIZED_CAN_DISGUISE',
                        my_own_can_disguise)

    request = rf.get('/')
    request.user = regular_user
    regular_user.last_name = last_name
    regular_user.save()
    SessionMiddleware().process_request(request)
    request.session.save()

    assert can_disguise(request) is can
