from django.apps import AppConfig, apps
from django.db.models.signals import post_migrate, post_save
from django.utils.translation import ugettext_lazy as _


class DisguiseConfig(AppConfig):
    name = 'disguise'
    verbose_name = _('Disguise')

    def ready(self):
        from .utils import create_perms

        post_migrate.connect(
            create_perms,
            sender=__import__('disguise')
        )
        post_save.connect(
            create_perms,
            sender=apps.get_model('auth.Permission')
        )
