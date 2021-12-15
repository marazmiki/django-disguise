from django.apps import AppConfig, apps
from django.core import checks
from django.db.models.signals import post_migrate, post_save
from django.utils.translation import gettext_lazy as _


class DisguiseConfig(AppConfig):
    name = 'disguise'
    verbose_name = _('Disguise')

    def ready(self):
        from .checks import check_env  # noqa
        from .utils import create_perms

        checks.register(check_env)

        post_migrate.connect(receiver=create_perms,
                             sender=__import__('disguise'))
        post_save.connect(receiver=create_perms,
                          sender=apps.get_model('auth.Permission'))
