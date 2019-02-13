from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import signals
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

signals.post_save.connect(create_perms, Permission)

try:
    sender = __import__('disguise')
    signals.post_syncdb.connect(create_perms, sender=sender)
except AttributeError:
    signals.post_migrate.connect(create_perms, sender=sender)
