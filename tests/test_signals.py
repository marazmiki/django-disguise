from django.contrib.auth.models import Permission
from django.db.models.signals import post_save


def test_permission():
    qs = Permission.objects.filter(codename='can_disguise')
    assert not qs.exists()

    post_save.send(sender=Permission)
    assert qs.exists()
