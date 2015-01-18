# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, post_syncdb
from django.utils.translation import ugettext_lazy as _
from disguise.compat import get_user_model


def create_perms(sender, **kwargs):
    perms = (
        ('can_disguise', _('Can disguise')),
    )

    content_type = ContentType.objects.get_for_model(get_user_model())

    for codename, title in perms:
        Permission.objects.get_or_create(
            codename=codename,
            content_type=content_type,
            defaults={
                'name': title,
            })


post_save.connect(create_perms, Permission)
post_syncdb.connect(create_perms, sender=__import__('disguise'))
